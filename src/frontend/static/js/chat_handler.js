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
            addMessageToChat(msg.content, type);
        });
    }

    async function renderChartWrapper(dataPoints) {
        if (dataPoints && Object.keys(dataPoints).length > 0) {
            document.getElementById("chartContainer").style.display = "block";
            renderChart(dataPoints); // Assuming renderChart is imported or globally available
        }
    }

    chatForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const userInput = chatInput.value.trim();
        if (!userInput) return;

        addMessageToChat(userInput, 'user');
        chatInput.value = '';

        const currentChatItem = document.querySelector('.chat-item.active-chat');
        const currentCid = currentChatItem?.dataset.cid;
        const isNew = currentChatItem?.dataset.isNew === 'true';

        if (!currentCid) {
            console.error("No active chat selected. Unable to send message.");
            return;
        }

        const body = {
            cid: currentCid,
            prompt: userInput,
            is_new: isNew
        };

        pendingResponseBubble = addMessageToChat('', 'bot');
        const loader = document.createElement('div');
        loader.className = 'loader';
        pendingResponseBubble.appendChild(loader);

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

                // Render chart if `data_points` are available
                await renderChartWrapper(data.data_points);

                if (isNew) {
                    currentChatItem.dataset.isNew = false;
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
                await renderChartWrapper(data.data_points); // Render chart with the conversation's `data_points`
            }
        } catch (error) {
            console.error('Error fetching conversation:', error);
        }
    }

    function setActiveChat(chatItem) {
        chatList.querySelectorAll('.chat-item').forEach((c) => c.classList.remove('active-chat'));
        chatItem.classList.add('active-chat');
    }

    function addChatToSidebar(cid, baseDateLabel) {
        const chatItem = document.createElement('button');
        chatItem.classList.add('sidebar-button', 'chat-item');
        chatItem.textContent = baseDateLabel;
        chatItem.dataset.cid = cid || '';
        chatItem.dataset.isNew = true;

        chatItem.addEventListener('click', () => {
            setActiveChat(chatItem);
            loadConversation(cid);
        });

        chatList.appendChild(chatItem);
        setActiveChat(chatItem);
        renderConversation([]);
    }

    newChatButton?.addEventListener('click', async () => {
        const date = new Date().toISOString().split('T')[0];

        try {
            const response = await fetch('/conversations', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });

            const data = await response.json();
            if (response.ok && data.cid) {
                addChatToSidebar(data.cid, date);
                chatContainer.innerHTML = '';
                document.getElementById("chartContainer").style.display = "none";
            }
        } catch (error) {
            console.error('Error creating new conversation:', error);
        }
    });

    clearHistoryButton?.addEventListener('click', () => {
        chatList.innerHTML = '';
        chatContainer.innerHTML = '';
        document.getElementById("chartContainer").style.display = "none";
    });
});
