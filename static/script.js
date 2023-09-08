const chatContainer = document.querySelector('.chat-container');
const chatIcon = document.querySelector('.chat-icon-button');
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const closeBtn = document.querySelector('.close-button');
const sendButton = document.getElementById('send-button');

function toggleChatContainer() {
    chatContainer.classList.toggle('show');
}

chatIcon.addEventListener('click', toggleChatContainer);

closeBtn.addEventListener('click', toggleChatContainer);

function initializeChat() {
    appendMessage('bot', 'Welcome! Please enter your email.');
}

function appendMessage(sender, message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    messageDiv.textContent = message;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight; 
}

function handleUserInput() {
    const userMessage = userInput.value.trim();

    if (userMessage === '') return;

    appendMessage('user', userMessage);

    sendUserMessageToServer(userMessage);

    userInput.value = '';
}

function sendUserMessageToServer(userMessage) {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/chatbot/', true); 
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function () {
        if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            const botResponse = response.bot_response;
            appendMessage('bot', botResponse);
        }
    };
    xhr.send(`user_message=${encodeURIComponent(userMessage)}`);
}

sendButton.addEventListener('click', handleUserInput);
userInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        handleUserInput();
    }
});

initializeChat();
