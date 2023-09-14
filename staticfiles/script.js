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
    const userMessageElement = document.createElement('div');
    userMessageElement.className = 'message user-message';
    userMessageElement.innerText = userMessage;
    chatMessages.appendChild(userMessageElement);

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

            // Add typing animation before displaying the response
            const typingElement = document.createElement('div');
            typingElement.className = 'message typing-message';
            typingElement.innerText = 'Typing...';
            chatMessages.appendChild(typingElement);

            // Delay the response display
            setTimeout(function () {
                // Remove the typing animation
                chatMessages.removeChild(typingElement);

                // Display the bot's response
                const chatbotResponseElement = document.createElement('div');
                chatbotResponseElement.className = 'message bot-message';
                chatbotResponseElement.innerText = chatbotResponse;
                chatMessages.appendChild(chatbotResponseElement);

                chatMessages.scrollTop = chatMessages.scrollHeight;
            }, 1500); // Adjust the delay time (in milliseconds) as needed

            saveConversationToDatabase(userMessage, chatbotResponse);
        },
        error: function () {
            // Handle errors if any
            alert('An error occurred while processing your request.');
        },
    });
}

function saveConversationToDatabase(userMessage, chatbotResponse) {
    // Send a POST request to a Django view that saves the conversation to the database
    $.ajax({
        url: '/save_conversation/',  // Create a URL for saving the conversation
        data: {
            userMessage: userMessage,
            chatbotResponse: chatbotResponse,
        },
        dataType: 'json',
        method: 'POST',  // Use POST method
        headers: { 'X-CSRFToken': csrftoken }, // Include CSRF token in headers
        success: function () {
            // Conversation saved successfully
            console.log('saved');
        },
        error: function () {
            // Handle errors if any
            alert('An error occurred while saving the conversation.');
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
