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

async function handleStream(response) {
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    
    while(true) {
        const { done, value } = await reader.read();
        if(done) break;
        
        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');
        
        lines.forEach(line => {
            if(line.startsWith('data: ')) {
                const message = line.replace('data: ', '');
                appendMessage('ai', message);
            }
        });
    }
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
