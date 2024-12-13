document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.getElementById('chatInput');
    const chatContainer = document.getElementById('chatContainer');
    const chartContainer = document.getElementById('chartContainer');
    const newChatButton = document.querySelector('.sidebar-button.new-chat');
    const clearHistoryButton = document.querySelector('.sidebar-button.clear-history');
    const sidebarContent = document.querySelector('.sidebar-content');
    const chatList = sidebarContent.querySelector('.chat-list');

    let pendingResponseBubble = null;
    const uid = document.body.dataset.uid;

    // Track if we are currently setting an active conversation to avoid race conditions
    let isSettingActiveConversation = false; 

    function updateChatPlaceholder() {
        if (chatList.childElementCount === 0) {
            chatContainer.innerHTML = `<div class="chat-placeholder animate"> Start by creating a new chat or selecting an already existing one!</div>`;
        } else {
            chatContainer.innerHTML = '';
        }
    }

    async function setActiveConversation(cid) {
        try {
            isSettingActiveConversation = true;
            disableUIInteraction();

            const response = await fetch('/active_conversation', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ cid: cid || null }),
            });

            if (!response.ok) {
                console.error('Failed to set active conversation:', response.statusText);
                return null;
            }

            const data = await response.json();
            console.log('Active conversation set on backend:', data.cid);
            return data.cid;
        } catch (err) {
            console.error("Error setting active conversation:", err);
            return null;
        } finally {
            isSettingActiveConversation = false;
            enableUIInteraction();
        }
    }

    function disableUIInteraction() {
        // Disable clicking on conversation buttons and form submission
        chatList.style.pointerEvents = 'none';
        chatForm.style.pointerEvents = 'none';
        newChatButton.disabled = true;
        clearHistoryButton.disabled = true;
    }

    function enableUIInteraction() {
        chatList.style.pointerEvents = '';
        chatForm.style.pointerEvents = '';
        newChatButton.disabled = false;
        clearHistoryButton.disabled = false;
    }

    function addChatToSidebar(cid, labelOrTitle, isNew = false) {
        // Avoid duplicates
        if (cid) {
            const existingChatItem = chatList.querySelector(`.chat-item[data-cid="${cid}"]`);
            if (existingChatItem) return;
        }
    
        const chatItem = document.createElement('button');
        chatItem.classList.add('sidebar-button', 'chat-item');
        chatItem.textContent = labelOrTitle || 'Untitled Conversation';
        chatItem.dataset.cid = cid || '';
        chatItem.dataset.isNew = isNew;
    
        chatItem.addEventListener('click', async () => {
            if (isSettingActiveConversation) {
                console.log("Already setting active conversation, please wait.");
                return;
            }
    
            disableUIInteraction();
    
            // Remove active class from all other chats
            chatList.querySelectorAll('.chat-item').forEach((c) => c.classList.remove('active-chat'));
            chatItem.classList.add('active-chat');
    
            const updatedCid = await setActiveConversation(cid || null);
            if (!updatedCid) {
                console.error("Failed to set active conversation on backend.");
                enableUIInteraction();
                return;
            }
    
            if (cid && chatItem.dataset.isNew === 'false') {
                await loadConversation(updatedCid);
            } else {
                renderConversation([]);
            }
    
            enableUIInteraction();
        });
    
        chatList.appendChild(chatItem);
        // Removed the line that automatically adds 'active-chat' here
        updateChatPlaceholder();
    }
    

    function addMessageToChat(content, type) {
        const messageBubble = document.createElement('div');
        messageBubble.className = `chat-bubble ${type}`;
        messageBubble.innerHTML = content;
        chatContainer.appendChild(messageBubble);
        chatContainer.scrollTop = chatContainer.scrollHeight;
        return messageBubble;
    }

    function renderConversation(messages) {
        chatContainer.innerHTML = '';
        messages.forEach((msg) => {
            const type = msg.role === 'user' ? 'user' : 'bot';
            let content = type === 'bot'
                ? DOMPurify.sanitize(marked.parse(msg.content || ''))
                : msg.content;

            const messageBubble = addMessageToChat(content, type);

            if (type === 'bot') {
                messageBubble.querySelectorAll('pre code').forEach((block) => {
                    hljs.highlightElement(block);
                });
            }
        });
    }

    async function renderChartWrapper(dataPoints) {
        if (dataPoints && Object.keys(dataPoints).length > 0) {
            document.getElementById("chartContainer").style.display = "block";
            renderChart(dataPoints);
        }
    }

    // Changes in chatForm submission handler
chatForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    // If we're currently setting the active conversation, don't allow sending messages
    if (isSettingActiveConversation) {
        console.log("Please wait, still setting active conversation.");
        return;
    }

    const userInput = chatInput.value.trim();
    if (!userInput) return;

    addMessageToChat(userInput, 'user');
    chatInput.value = '';

    // Store cid and isNew at the moment of sending
    const currentChatItem = document.querySelector('.chat-item.active-chat');
    const sendCid = currentChatItem?.dataset.cid;
    const sendIsNew = currentChatItem?.dataset.isNew === 'true';

    if (!sendCid) {
        console.error("No active chat selected. Unable to send message.");
        return;
    }

    pendingResponseBubble = addMessageToChat('', 'bot');
    const loader = document.createElement('div');
    loader.className = 'loader';
    pendingResponseBubble.appendChild(loader);

    const body = { cid: sendCid, prompt: userInput, is_new: sendIsNew };

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
        });

        const data = await response.json();
        pendingResponseBubble.innerHTML = '';

        if (response.ok) {
            const cleanHTML = DOMPurify.sanitize(marked.parse(data.response || 'No response'));
            pendingResponseBubble.innerHTML = cleanHTML;
            pendingResponseBubble.querySelectorAll('pre code').forEach((block) => {
                hljs.highlightElement(block);
            });

            await renderChartWrapper(data.data_points);

            // Update is_new based on the cid we sent with, not the currently active chat
            if (sendIsNew) {
                const sentChatItem = chatList.querySelector(`.chat-item[data-cid="${sendCid}"]`);
                if (sentChatItem) {
                    sentChatItem.dataset.isNew = false;
                }
            }
        } else {
            pendingResponseBubble.innerHTML = `<p>${data.message || 'Error communicating with the server.'}</p>`;
            document.getElementById("chartContainer").style.display = "none";
        }
    } catch (error) {
        console.error('Error during chat submission:', error);
        pendingResponseBubble.innerHTML = '<p>Error communicating with the server.</p>';
        document.getElementById("chartContainer").style.display = "none";
    } finally {
        pendingResponseBubble = null;
    }
});


    chatInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            if (event.shiftKey) {
                const cursorPos = chatInput.selectionStart;
                const textBeforeCursor = chatInput.value.slice(0, cursorPos);
                const textAfterCursor = chatInput.value.slice(cursorPos);
                chatInput.value = `${textBeforeCursor}\n${textAfterCursor}`;
                chatInput.selectionStart = chatInput.selectionEnd = cursorPos + 1;
            } else {
                event.preventDefault();
                chatForm.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
            }
        }
    });

    async function loadConversation(cid) {
        try {
            const response = await fetch(`/messages/${cid}`);
            if (!response.ok) throw new Error(`Failed to fetch messages: ${response.statusText}`);
            const data = await response.json();

            if (data.message === 'success') {
                renderConversation(data.conversation_history);
                await renderChartWrapper(data.data_points);
            }
        } catch (error) {
            console.error('Error fetching conversation:', error);
        }
    }

    async function fetchChatHistory(uid) {
        if (!uid) {
            console.error("No UID provided for fetching chat history.");
            return;
        }

        try {
            const response = await fetch('/conversations');
            const data = await response.json();

            if (!response.ok || !data.conversations) {
                console.error("Failed to fetch chat history:", data.message);
                return;
            }

            chatList.innerHTML = '';
            Object.entries(data.conversations).forEach(([cid, title]) => {
                addChatToSidebar(cid, title || "Untitled Conversation");
            });
        } catch (error) {
            console.error("Error fetching chat history:", error);
        }
    }

    // Changes in newChatButton event listener
newChatButton?.addEventListener('click', async () => {
    if (isSettingActiveConversation) {
        console.log("Please wait, still setting active conversation.");
        return;
    }

    disableUIInteraction();

    const date = new Date().toISOString().split('T')[0];

    try {
        const response = await fetch('/conversations', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });

        const data = await response.json();
        if (response.ok && data.cid) {
            const updatedCid = await setActiveConversation(data.cid);
            if (!updatedCid) {
                console.error("Failed to set the new conversation as active.");
                enableUIInteraction();
                return;
            }

            // Add the new conversation to the sidebar and mark it as new
            addChatToSidebar(data.cid, date, true);

            // Immediately mark this new chat as active in the UI
            const newChatItem = chatList.querySelector(`.chat-item[data-cid="${data.cid}"]`);
            chatList.querySelectorAll('.chat-item').forEach((c) => c.classList.remove('active-chat'));
            newChatItem.classList.add('active-chat');

            // Render an empty conversation for the new chat
            renderConversation([]);
            
            chatContainer.innerHTML = '';
            document.getElementById("chartContainer").style.display = "none";
            updateChatPlaceholder();
        }
    } catch (error) {
        console.error('Error creating new conversation:', error);
    } finally {
        enableUIInteraction();
    }
});


    clearHistoryButton?.addEventListener('click', async () => {
        const confirmation = confirm("Are you sure you want to delete all conversations? This action cannot be undone.");
        if (!confirmation) return;

        disableUIInteraction();

        try {
            const response = await fetch(`/conversations`, {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' }
            });

            const data = await response.json();

            if (response.ok) {
                console.log("All conversations deleted successfully.");
                chatList.innerHTML = '';
                chatContainer.innerHTML = '';
                document.getElementById("chartContainer").style.display = "none";
                updateChatPlaceholder();
            } else {
                console.error("Failed to delete conversations. Message:", data.message);
            }
        } catch (error) {
            console.error("Error deleting all conversations:", error);
        } finally {
            enableUIInteraction();
        }
    });

    updateChatPlaceholder();
    fetchChatHistory(uid);
});
