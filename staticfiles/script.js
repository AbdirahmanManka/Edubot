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


// Event listeners for user input
sendButton.addEventListener('click', handleUserInput);
userInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        handleUserInput();
    }
});

$(document).ready(function () {
    // Function to send a message to the chatbot and update the chat window
    function sendMessageToChatbot() {
        const userMessage = $('#user-input').val();
        $('#chat-messages').append(`<div class="user-message">${userMessage}</div>`);

    
        $.ajax({
            url: '/chatbot_response/',  // Update with the correct URL
            data: { message: userMessage },
            dataType: 'json',
            method: 'GET',
            success: function (data) {
                const chatbotResponse = data.response;
                $('#chat-messages').append(`<div class="chatbot-message">${chatbotResponse}</div>`);
                // Clear the user input field
                $('#user-input').val('');
            },
            error: function () {
                // Handle errors if any
                alert('An error occurred while processing your request.');
            },
        });
    }

    // Handle user input
    $('#send-button').click(function () {
        sendMessageToChatbot();
    });

    // Handle Enter key press in the input field
    $('#user-input').keypress(function (e) {
        if (e.which === 13) {
            sendMessageToChatbot();
        }
    });
});
