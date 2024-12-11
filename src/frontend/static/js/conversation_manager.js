// conversation_manager.js

// This module handles all conversation-related operations:
// - Creating new conversations
// - Loading a conversation's message history
// - Returning data to be displayed by sidebar and chat handler

// Function to create a new conversation via /conversations endpoint.
// Returns a promise that resolves to { cid, date }
async function createNewConversation() {
    const response = await fetch('/conversations', {
        method: 'POST'
    });
    const data = await response.json();

    if (!response.ok || !data.cid) {
        throw new Error(data.message || "Failed to create conversation");
    }

    // Generate today's date (YYYY-MM-DD) for labeling the chat
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    const dateLabel = `${year}-${month}-${day}`;

    return { cid: data.cid, date: dateLabel };
}

// Function to load a conversation's entire message history from /messages/<cid>
// Returns a promise that resolves to an array of message objects:
// [{ role: "user" or "assistant", text: "<message>"}]
async function loadConversation(cid) {
    try {
        const response = await fetch(`/messages/${cid}`);
        if (!response.ok) throw new Error(`Failed to fetch messages: ${response.statusText}`);
        const data = await response.json();

        if (data.message === 'success') {
            // Render the conversation messages
            renderConversation(data.conversation_history);

            // Render the chart if data points are available
            if (data.data_points && Object.keys(data.data_points).length > 0) {
                await renderChartWrapper(data.data_points);
            }
        }
    } catch (error) {
        console.error('Error fetching conversation:', error);
    }
}


// Export the functions so other modules can use them
export { createNewConversation, loadConversationHistory };
