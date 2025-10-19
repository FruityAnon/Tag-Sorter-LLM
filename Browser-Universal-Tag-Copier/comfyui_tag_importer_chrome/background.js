// Background script for Chrome - обходить CSP
console.log('🎯 Tag Importer: Background service worker loaded');

// Функція для відправки тегів на ComfyUI
async function sendTagsToComfyUI(tags, source) {
    try {
        console.log('💾 Background: Saving tags to file...');
        
        const response = await fetch('http://localhost:8188/e621/save_tags_to_file', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                tags: tags,
                filename: 'tags_storage.txt',
                source: source,
                timestamp: new Date().toISOString()
            })
        });

        if (response.ok) {
            const result = await response.json();
            return { success: true, data: result };
        } else {
            const errorText = await response.text();
            return { success: false, error: `HTTP ${response.status}: ${errorText}` };
        }
    } catch (error) {
        return { success: false, error: error.message };
    }
}

// Обробник повідомлень від content script та popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log('📨 Background: Received message:', message);
    
    if (message.action === "saveTagsToFile") {
        sendTagsToComfyUI(message.tags, message.source)
            .then(sendResponse);
        return true; // Позначаємо, що відповідь буде асинхронною
    }
    
    if (message.action === "checkComfyUI") {
        fetch('http://localhost:8188/e621/status')
            .then(response => response.json())
            .then(data => sendResponse({ success: true, data: data }))
            .catch(error => sendResponse({ success: false, error: error.message }));
        return true;
    }
});

console.log('🎉 Tag Importer: Background service worker ready');