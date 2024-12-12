// conversation_manager.js

// Function to create a new conversation via /conversations endpoint.
// Returns a promise that resolves to { cid, date }
/*
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

// Function to fetch all chat history for a user via /conversations/<uid> endpoint.
// Returns a promise that resolves to an object containing chat history { cid1: title1, cid2: title2 }

async function fetchChatHistory(uid) {
    try {
        const response = await fetch(`/conversations/${uid}`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || "Failed to fetch chat history");
        }

        return data.conversations; // Assuming the API returns { conversations: { cid1: title1, cid2: title2 } }
    } catch (error) {
        console.error('Error fetching chat history:', error);
        throw error;
    }
}

// Export the functions so other modules can use them
//export { createNewConversation, fetchChatHistory };

*/