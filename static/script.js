const chatContainer = document.querySelector('.chat-container');
const chatIcon = document.querySelector('.chat-icon-button');
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const closeBtn = document.querySelector('.close-button');
const sendButton = document.getElementById('send-button');

let userEmailAddress = '';
let chatbotState = 'waiting_for_email';

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

    if (chatbotState === 'waiting_for_email') {
        // Validate user email format
        if (!isValidEmail(userMessage)) {
            appendMessage('bot', 'Please enter a valid email address.');
        } else {
            // Set the user's email and change chatbot state
            userEmailAddress = userMessage;
            chatbotState = 'waiting_for_service_choice';
            appendMessage('bot', `Welcome ${userEmailAddress}! How can we help you? Available services: Accounts, Programs, Other Issue.`);
        }
    } else if (chatbotState === 'waiting_for_service_choice') {
        appendMessage('user', userMessage);
        sendUserMessageToServer(userMessage);
    }

    userInput.value = '';
}

function isValidEmail(email) {
    // Perform basic email format validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
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
    xhr.send(`user_message=${encodeURIComponent(userMessage)}&user_email=${encodeURIComponent(userEmailAddress)}`);
}

sendButton.addEventListener('click', handleUserInput);
userInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        handleUserInput();
    }
});

initializeChat();