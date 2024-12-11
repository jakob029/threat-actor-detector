document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.getElementById('chatInput');
    const chatContainer = document.getElementById('chatContainer');
    const chartContainer = document.getElementById('chartContainer'); // Ensure this exists in your HTML
    let pendingResponseBubble = null;

    function addMessageToChat(content, type) {
        const messageBubble = document.createElement('div');
        messageBubble.className = `chat-bubble ${type}`;
        messageBubble.innerHTML = content;
        chatContainer.appendChild(messageBubble);
        chatContainer.scrollTop = chatContainer.scrollHeight;
        return messageBubble;
    }

    chatForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const userInput = chatInput.value.trim();
        if (!userInput) return;

        // Add the user's message to the chat
        addMessageToChat(userInput, 'user');
        chatInput.value = '';

        const currentChatItem = document.querySelector('.chat-item.active-chat');
        const currentCid = currentChatItem.dataset.cid;
        const isNew = currentChatItem.dataset.isNew === 'true';

        const body = {
            cid: currentCid,
            prompt: userInput,
            is_new: isNew  // Send the flag to the backend
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
                // Render markdown for the bot's response
                const dirtyHTML = marked.parse(data.response || 'No response');
                const cleanHTML = DOMPurify.sanitize(dirtyHTML);
                pendingResponseBubble.innerHTML = cleanHTML;

                // Highlight code blocks if present
                pendingResponseBubble.querySelectorAll('pre code').forEach((block) => {
                    hljs.highlightElement(block);
                });

                // Render the chart using data points
                if (data.data_points && Object.keys(data.data_points).length > 0) {
                    document.getElementById("chartContainer").style.display = "block"; // Show chart container
                    renderChart(data.data_points); // Call renderChart with the data points
                } else {
                    document.getElementById("chartContainer").style.display = "none"; // Hide if no data points
                }

                if (isNew) {
                    currentChatItem.dataset.isNew = false; // Mark as no longer new
                }
            } else {
                pendingResponseBubble.innerHTML = `<p>${data.message || 'Error communicating with the server.'}</p>`;
                document.getElementById("chartContainer").style.display = "none"; // Hide chart on error
            }
        } catch (error) {
            console.error('Error during chat submission:', error);
            pendingResponseBubble.innerHTML = '<p>Error communicating with the server.</p>';
            document.getElementById("chartContainer").style.display = "none"; // Hide chart on exception
        } finally {
            pendingResponseBubble = null; // Reset the pending response bubble
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
});

function renderConversation(messages) {
    const chatContainer = document.getElementById('chatContainer');

    chatContainer.innerHTML = '';

    messages.forEach((msg) => {
        const type = msg.role === 'user' ? 'user' : 'bot';
        addMessageToChat(msg.text, type);
    });
}

export { renderConversation };
