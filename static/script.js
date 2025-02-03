const inputField = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const messagesDiv = document.getElementById('messages');

// Handle message sending
async function sendMessage() {
    const message = inputField.value.trim();
    if (!message) return;

    appendMessage('user', message);
    inputField.value = '';
    showLoading();

    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });
        
        if(response.ok) {
            await handleStream(response);
        }
    } catch (error) {
        console.error('Error:', error);
        hideLoading();
    }
}

let currentAiMessage = null;

async function handleStream(response) {
    currentAiMessage = document.createElement('div');
    currentAiMessage.className = 'message ai-message';
    messagesDiv.appendChild(currentAiMessage);
    
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    let partial = '';
    
    while(true) {
        const { done, value } = await reader.read();
        if(done) break;
        
        buffer += decoder.decode(value, { stream: true });
        
        // Process word by word
        const words = buffer.split(' ');
        buffer = words.pop() || '';
        
        for(const word of words) {
            partial += word + ' ';
            currentAiMessage.innerHTML = marked.parse(partial);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
            await new Promise(r => setTimeout(r, 50)); // Typing speed
        }
    }
    
    // Add remaining buffer
    if(buffer) {
        partial += buffer;
        currentAiMessage.innerHTML = marked.parse(partial);
    }
    
    currentAiMessage = null;
    hideLoading();
}

// Event listeners
sendBtn.addEventListener('click', sendMessage);
inputField.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

function appendMessage(sender, text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    messageDiv.textContent = text;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function showLoading() {
    document.getElementById('loading').style.display = 'block';
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}
