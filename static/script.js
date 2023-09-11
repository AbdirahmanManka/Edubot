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

// Function to get the CSRF token from cookies
function getCookie(name) {
    const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
}

// Function to send a message to the chatbot and update the chat window
function sendMessageToChatbot() {
    const userMessage = userInput.value;
    chatMessages.innerHTML += `<br><div class="user-message">${userMessage}</div>`;

    // Get the CSRF token from cookies
    const csrftoken = getCookie('csrftoken');

    // Clear the user input field
    userInput.value = '';

    // Send the user message to the server for processing using POST
    $.ajax({
        url: '/chatbot_response/',  // Update with the correct URL
        data: { userMessage: userMessage },
        dataType: 'json',
        method: 'POST',  // Use POST method
        headers: { 'X-CSRFToken': csrftoken }, // Include CSRF token in headers
        success: function (data) {
            const chatbotResponse = data.response;
            chatMessages.innerHTML += `<br><div class="bot-message">${chatbotResponse}</div>`;

            chatMessages.scrollTop = chatMessages.scrollHeight;
        },
        error: function () {
            // Handle errors if any
            alert('An error occurred while processing your request.');
        },
    });
}

// Event listeners for user input
sendButton.addEventListener('click', sendMessageToChatbot);
userInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessageToChatbot();
    }
});
