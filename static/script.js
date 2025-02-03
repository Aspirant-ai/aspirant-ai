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
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: message // Use 'query' to match the backend
            })
        });
        
        if (response.ok) {
            await handleStream(response);
        } else {
            hideLoading();
            showError('Failed to get a valid response from the server');
        }
    } catch (error) {
        console.error('Error:', error);
        hideLoading();
        showError('Network error');
    }
}


let currentAiMessage = null;
let accumulatedResponse = '';

// Updated handleStream function
async function handleStream(response) {
    const data = await response.json();
    if (!data.stream_url) {
        showError('No stream URL received');
        return;
    }

    currentAiMessage = document.createElement('div');
    messagesDiv.appendChild(currentAiMessage);
    accumulatedResponse = '';

    const eventSource = new EventSource(data.stream_url);
    
    eventSource.onmessage = (e) => {
        if (e.data.trim() === '') return;
        accumulatedResponse += e.data;
        currentAiMessage.innerHTML = marked ? marked.parse(accumulatedResponse) : accumulatedResponse;
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    };

    eventSource.onerror = (err) => {
        console.error('EventSource error:', err);
        eventSource.close();
        showError('Connection error');
        hideLoading();
    };
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

function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'message error-message';
    errorDiv.textContent = message;
    messagesDiv.appendChild(errorDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}
