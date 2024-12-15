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
    let currentConversationPromise = null; 

    function updateChatPlaceholder() {
        if (chatList.childElementCount === 0) {
            chatContainer.innerHTML = `<div class="chat-placeholder animate"> Start by creating a new chat or selecting an already existing one!</div>`;
        } else {
            chatContainer.innerHTML = '';
        }
    }

    async function setActiveConversation(cid) {
        // If we already have a conversation-changing process ongoing, wait or refuse new actions
        if (currentConversationPromise) {
            console.log("Another conversation is being set, please wait...");
            return null;
        }

        const promise = (async () => {
            disableUIInteraction();
            try {
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
                enableUIInteraction();
            }
        })();

        currentConversationPromise = promise;
        const result = await promise;
        currentConversationPromise = null;
        return result;
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
            // Remove any check for isSettingActiveConversation. We use currentConversationPromise now.
            if (currentConversationPromise) {
                console.log("Already in the process of setting a conversation. Please wait...");
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
    // Submit event listener (unchanged except ensuring no dispatchEvent is used elsewhere)
chatForm.addEventListener('submit', async (event) => {
    console.log('Submit event triggered');
    event.preventDefault();

    // Since we're no longer using dispatchEvent, this will only fire once per Enter press.
    if (currentConversationPromise) {
        console.log("Please wait until the active conversation is set.");
        return;
    }

    

    const userInput = chatInput.value.trim();
    console.log('User input:', userInput);
    if (!userInput) return;

    addMessageToChat(userInput, 'user');
    chatInput.value = '';

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
        console.log('Fetching /chat with user input:', userInput);
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
        // Remove isSettingActiveConversation checks
        if (currentConversationPromise) {
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
    
                addChatToSidebar(data.cid, date, true);
    
                const newChatItem = chatList.querySelector(`.chat-item[data-cid="${data.cid}"]`);
                chatList.querySelectorAll('.chat-item').forEach((c) => c.classList.remove('active-chat'));
                newChatItem.classList.add('active-chat');
    
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
