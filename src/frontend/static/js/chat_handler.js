document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.getElementById('chatInput');
    const chatContainer = document.getElementById('chatContainer');
    let pendingResponseBubble = null; // To store the bubble currently showing the loader

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

        // Add the user's message
        addMessageToChat(userInput, 'user');
        chatInput.value = '';

        // Create a bot bubble with a loader
        pendingResponseBubble = addMessageToChat('', 'bot');
        const loader = document.createElement('div');
        loader.className = 'loader';
        pendingResponseBubble.appendChild(loader);
        chatContainer.scrollTop = chatContainer.scrollHeight;

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt: userInput }),
            });
            const data = await response.json();

            // Remove loader before inserting the actual response
            pendingResponseBubble.innerHTML = '';

            if (response.ok) {
                // Render markdown
                const dirtyHTML = marked.parse(data.response || 'No response');
                const cleanHTML = DOMPurify.sanitize(dirtyHTML);

                // Insert sanitized HTML
                pendingResponseBubble.innerHTML = cleanHTML;

                // Highlight code blocks
                pendingResponseBubble.querySelectorAll('pre code').forEach((block) => {
                    hljs.highlightElement(block);
                });

                // Debugging: Log the data_points
                console.log("Data points received:", data.data_points);

                // Handle data points for chart
                if (data.data_points && Object.keys(data.data_points).length > 0) {
                    console.log("Rendering chart with data points:", data.data_points);
                    document.getElementById("chartContainer").style.display = "block";
                    renderChart(data.data_points);
                } else {
                    console.log("No data points available, hiding chart.");
                    document.getElementById("chartContainer").style.display = "none";
                }

            } else {
                pendingResponseBubble.innerHTML = `<p>${data.message || "Error communicating with the server."}</p>`;
                document.getElementById("chartContainer").style.display = "none";
            }
        } catch (error) {
            console.error('Error:', error);
            pendingResponseBubble.innerHTML = '<p>Error communicating with the server.</p>';
            document.getElementById("chartContainer").style.display = "none";
        } finally {
            pendingResponseBubble = null;
        }
    });

    // Handle "Enter" and "Shift+Enter" in chatInput
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

    // Clear current chat
    chatContainer.innerHTML = '';

    // Render each message
    messages.forEach(msg => {
        const type = (msg.role === 'user') ? 'user' : 'bot';
        addMessageToChat(msg.text, type);
    });
}

// Export if needed, or just ensure this file is included and addMessageToChat is accessible
export { renderConversation };