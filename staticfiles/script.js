// Select elements
const chatContainer = document.querySelector('.chat-container');
const chatIcon = document.querySelector('.chat-icon-button');
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const closeBtn = document.querySelector('.close-button');
const sendButton = document.getElementById('send-button');

// Open or close the chat container
function toggleChatContainer() {
    chatContainer.classList.toggle('show');
}

chatIcon.addEventListener('click', toggleChatContainer);
closeBtn.addEventListener('click', toggleChatContainer);

// Append a message to the chat
function appendMessage(sender, message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    messageDiv.textContent = message;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Handle user input
function handleUserInput() {
    const userMessage = userInput.value.trim();

    if (userMessage === '') return;

    appendMessage('user', userMessage);
    sendUserMessageToServer(userMessage);

    userInput.value = '';
}

let userEmailAddress = 'student1@gmail.com';

// Function to send user message to the server
function sendUserMessageToServer(userMessage) {
    // Prepare the request data
    const data = new URLSearchParams();
    data.append('user_email', userEmailAddress);  // Assuming userEmailAddress is defined

    // Make a POST request to check if email exists
    fetch('/check_email/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: data,
    })
    .then(response => response.json())
    .then(data => {
        const result = data.result;
        if (result === 'Email exists') {
            const name = data.name;
            // Email exists in the database, you can proceed with the chat
            appendMessage('bot', `Welcome ${name}! How can we help you? Available services: Accounts, Programs, Other Issue.`);
        } else {
            // Email doesn't exist, provide feedback to the user
            appendMessage('bot', 'The provided email does not exist in our database. Please enter a valid email.');
        }
    })
    .catch(error => {
        console.error('Error checking email:', error);
    });
}

// Event listeners for user input
sendButton.addEventListener('click', handleUserInput);
userInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        handleUserInput();
    }
});
