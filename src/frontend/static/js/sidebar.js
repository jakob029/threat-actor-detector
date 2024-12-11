// sidebar.js
import { loadConversationHistory } from './conversation_manager.js';
import { renderConversation } from './chat_handler.js';

document.addEventListener('DOMContentLoaded', () => {
    const newChatButton = document.querySelector('.sidebar-button.new-chat');
    const clearHistoryButton = document.querySelector('.sidebar-button.clear-history');
    const sidebarContent = document.querySelector('.sidebar-content');
    const chatList = sidebarContent.querySelector('.chat-list');

    // Keep track of conversations in memory: [{ cid: string|null, date: string }]
    let conversations = [];

    // Debounce timer to prevent rapid click events
    let debounceTimer = null;

    function getTodayDate() {
        const today = new Date();
        const year = today.getFullYear();
        const month = String(today.getMonth() + 1).padStart(2, '0');
        const day = String(today.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

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

    function setActiveChat(chatItem) {
        const allChats = chatList.querySelectorAll('.chat-item');
        allChats.forEach((c) => c.classList.remove('active-chat'));
        chatItem.classList.add('active-chat');
    }

    function addChatToSidebar(cid, baseDateLabel, isNew = true) {
        const uniqueName = generateUniqueChatName(baseDateLabel);
    
        const chatItem = document.createElement('button');
        chatItem.classList.add('sidebar-button', 'chat-item');
        chatItem.textContent = uniqueName;
        chatItem.dataset.cid = cid || ''; // Set the data-cid attribute
        chatItem.dataset.isNew = isNew;  // Explicitly set if it's a new conversation
    
        conversations.push({ cid, date: baseDateLabel });
    
        chatItem.addEventListener('click', async () => {
            if (debounceTimer) return; // Prevent rapid consecutive clicks
    
            debounceTimer = setTimeout(async () => {
                try {
                    chatItem.disabled = true; // Disable button temporarily
                    setActiveChat(chatItem);
    
                    const currentCid = chatItem.dataset.cid;
    
                    if (!currentCid) {
                        console.error("Invalid cid: Cannot switch to a null conversation.");
                        return;
                    }
    
                    // Notify the backend to set the active conversation
                    const activeResponse = await fetch('/active_conversation', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ cid: currentCid })
                    });
    
                    if (!activeResponse.ok) {
                        const errData = await activeResponse.json();
                        throw new Error(errData.message || "Failed to set active conversation");
                    }
    
                    // Fetch and render the conversation's history
                    const history = await loadConversationHistory(currentCid);
                    renderConversation(history);
    
                    // Reset the new conversation flag after switching
                    chatItem.dataset.isNew = false;
                } catch (error) {
                    console.error("Error switching conversation:", error);
                } finally {
                    chatItem.disabled = false; // Re-enable button
                    debounceTimer = null; // Reset debounce timer
                }
            }, 300);
        });
    
        chatList.appendChild(chatItem);
        setActiveChat(chatItem);
        renderConversation([]); // Show blank conversation
    }
    

    newChatButton?.addEventListener('click', async () => {
        console.log('New Chat clicked');
        const date = getTodayDate();
    
        try {
            // Create a new conversation
            const response = await fetch('/conversations', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            const data = await response.json();
    
            if (!response.ok || !data.cid) {
                throw new Error(data.message || "Failed to create conversation");
            }
    
            const cid = data.cid;
            console.log("New conversation created with cid:", cid);
    
            addChatToSidebar(cid, date, true); // Set `isNew` to true explicitly
        } catch (error) {
            console.error("Error creating new conversation:", error);
        }
    });
    

    clearHistoryButton?.addEventListener('click', () => {
        console.log('Clear History clicked');
        chatList.querySelectorAll('.chat-item').forEach((item) => item.remove());
        conversations = [];
        renderConversation([]);
    });
});
