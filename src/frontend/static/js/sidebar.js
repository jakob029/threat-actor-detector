// sidebar.js
import { loadConversationHistory } from './conversation_manager.js';
import { renderConversation } from './chat_handler.js';

document.addEventListener('DOMContentLoaded', () => {
    const newChatButton = document.querySelector('.sidebar-button.new-chat');
    const clearHistoryButton = document.querySelector('.sidebar-button.clear-history');
    const sidebarContent = document.querySelector('.sidebar-content');
    const chatList = sidebarContent.querySelector('.chat-list');

    // Keep track of conversations in memory: [{ cid: string|null, date: string, isNew: boolean }]
    let conversations = [];

    // Function to get today's date in YYYY-MM-DD format
    function getTodayDate() {
        const today = new Date();
        const year = today.getFullYear();
        const month = String(today.getMonth() + 1).padStart(2, '0');
        const day = String(today.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

    // Function to generate a unique chat name
    function generateUniqueChatName(baseName) {
        const existingChatNames = Array.from(chatList.querySelectorAll('.chat-item')).map(
            (item) => item.textContent
        );

        let uniqueName = baseName;
        let counter = 1;

        while (existingChatNames.includes(uniqueName)) {
            uniqueName = `${baseName} (${counter})`;
            counter++;
        }

        return uniqueName;
    }

    // Function to set a chat as active
    function setActiveChat(chatItem) {
        const allChats = chatList.querySelectorAll('.chat-item');
        allChats.forEach((c) => c.classList.remove('active-chat'));
        chatItem.classList.add('active-chat');
    }

    // Add a new chat to the sidebar
    // cid = null and isNew = true for brand-new chats (not created on backend yet)
    function addChatToSidebar(cid, baseDateLabel, isNew = false) {
        const uniqueName = generateUniqueChatName(baseDateLabel);

        const chatItem = document.createElement('button');
        chatItem.classList.add('sidebar-button', 'chat-item');
        chatItem.textContent = uniqueName;
        chatItem.dataset.cid = cid ? cid : '';

        let conv = conversations.find(conv => conv.cid === cid);
        if (!conv) {
            conv = { cid, date: baseDateLabel, isNew };
            conversations.push(conv);
        } else {
            conv.isNew = isNew;
        }

        chatItem.addEventListener('click', async () => {
            console.log(`Switching to conversation: ${cid}`);
            setActiveChat(chatItem);
            renderConversation([]); // Clear chat first

            const currentConv = conversations.find(conv => conv.cid === cid);

            if (currentConv && currentConv.isNew) {
                console.log("This is a brand-new conversation. No messages to load.");
                // Show empty chat. The first user prompt will trigger /chat to create a conversation and use /analyzis.
                return;
            }

            try {
                const activeResponse = await fetch('/active_conversation', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ cid })
                });

                if (!activeResponse.ok) {
                    const errData = await activeResponse.json();
                    throw new Error(errData.message || "Failed to set active conversation");
                }

                const history = await loadConversationHistory(cid);
                renderConversation(history);
            } catch (error) {
                console.error("Error loading conversation history or setting active conversation:", error);
            }
        });

        chatList.appendChild(chatItem);
        setActiveChat(chatItem);
        renderConversation([]); // Show blank conversation
    }

    // "New Chat" now just creates a local new chat with cid = null and isNew = true
    newChatButton?.addEventListener('click', async () => {
        console.log('New Chat clicked');
        const date = getTodayDate();

        // Notify backend to clear `cid` for the session
        try {
            const response = await fetch('/active_conversation', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ cid: null }) // Clear the session's `cid`
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.message || "Failed to reset active conversation");
            }
        } catch (error) {
            console.error("Error clearing active conversation:", error);
        }

        // Add a new local chat
        addChatToSidebar(null, date, true);
    });

    // Handle "Clear History" button click: remove all chat items
    clearHistoryButton?.addEventListener('click', () => {
        console.log('Clear History clicked');
        chatList.querySelectorAll('.chat-item').forEach((item) => item.remove());
        conversations = [];
        renderConversation([]);
    });
});
