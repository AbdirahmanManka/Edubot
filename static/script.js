// Get DOM elements
const chatContainer = document.querySelector('.chat-container');
const chatHeader = document.querySelector('.chat-header');
const closeBtn = document.querySelector('.close-button');
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

// Function to toggle chat container visibility
function toggleChatContainer() {
    chatContainer.classList.toggle('show');
}

// Event listener to toggle chat container on chat icon click
chatIcon.addEventListener('click', toggleChatContainer);

// Event listener to close chat container
closeBtn.addEventListener('click', toggleChatContainer);

// Initialize chat
function initializeChat() {
    appendMessage('bot', chatbotResponses.welcome);
}

// Append a message to the chat
function appendMessage(sender, message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    messageDiv.textContent = message;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll to the latest message
}

// Handle user input
function handleUserInput() {
    const userMessage = userInput.value.trim();

    if (userMessage === '') return;

    // Append user message to chat messages
    appendMessage('user', userMessage);

    // Handle user's message
    handleChatbotResponse(userMessage);

    // Clear user input
    userInput.value = '';
}

// Handle chatbot responses
