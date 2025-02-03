const eventSource = new EventSource('/stream');
const inputField = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

sendBtn.addEventListener('click', async () => {
  const message = inputField.value.trim();
  if (message) {
    appendMessage('user', message);
    inputField.value = '';
    showLoading();
    
    // Send message to server
    await fetch('/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });
  }
});

eventSource.onmessage = (e) => {
  hideLoading();
  appendMessage('ai', e.data);
};

function appendMessage(sender, text) {
  const messagesDiv = document.getElementById('messages');
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