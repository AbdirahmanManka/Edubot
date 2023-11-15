// Select elements
const chatContainer = document.querySelector('.chat-container');
const chatIcon = document.querySelector('.chat-icon-button');
const chatMessages = document.getElementById('chat-window');
const userInput = document.getElementById('chat-input');
const closeBtn = document.querySelector('.close-button');
const sendButton = document.getElementById('send-button');

$(document).ready(function () {
    $("#chatbot-toggle").click(function () {
        $("#chat-container").toggle();
    });

    $("#close-chat").click(function () {
        $("#chat-container").hide();
    });
});

function getCookie(name) {
    const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
}

function sendMessageToChatbot() {
    const userMessage = userInput.value.trim();
    if (userMessage === '') {
        return;
    }

    console.log('User clicked send button:', userMessage);

    appendMessage('user', userMessage);

    const csrftoken = getCookie('csrftoken');

    userInput.value = '';

    $.ajax({
        url: '/chatbot_response/',
        data: { userMessage: userMessage },
        dataType: 'json',
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken },
        success: function (data) {
            const chatbotResponse = data.response;

            console.log('Chatbot response received:', chatbotResponse);

            appendMessage('typing', 'Typing...');

            setTimeout(function () {
                removeLastMessage();

                appendMessage('bot', chatbotResponse);

                chatMessages.scrollTop = chatMessages.scrollHeight;
            }, 1500);

            saveConversationToDatabase(userMessage, chatbotResponse);
        },
        error: function () {
            console.error('An error occurred while processing your request.');
        },
    });
}

const MAX_MESSAGES = 20; 
const allMessages = [];

function appendMessage(sender, message) {
    const messageElement = document.createElement('div');
    const messageClass = sender === 'user' ? 'sent-message' : 'received-message';
    messageElement.className = `message ${messageClass}`;
    messageElement.innerText = message;
    
    allMessages.push({ sender, message });

    updateChatContainer();

    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function updateChatContainer() {
    const startIndex = Math.max(0, allMessages.length - MAX_MESSAGES);

    const visibleMessages = allMessages.slice(startIndex);

    chatMessages.innerHTML = '';

    visibleMessages.forEach(({ sender, message }) => {
        const messageElement = document.createElement('div');
        const messageClass = sender === 'user' ? 'sent-message' : 'received-message';
        messageElement.className = `message ${messageClass}`;
        messageElement.innerText = message;
        chatMessages.appendChild(messageElement);
    });
}

chatMessages.addEventListener('scroll', function () {
    updateChatContainer();
});

function removeLastMessage() {
    const lastMessage = chatMessages.lastChild;
    if (lastMessage) {
        chatMessages.removeChild(lastMessage);
    }
}

sendButton.addEventListener('click', function () {
    console.log('User clicked send button (using event listener)');
    sendMessageToChatbot();
});

userInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        console.log('User pressed Enter key');
        sendMessageToChatbot();
    }
});

function saveConversationToDatabase(userMessage, chatbotResponse) {
    const csrftoken = getCookie('csrftoken');

    $.ajax({
        url: '/save_conversation/',
        data: {
            userMessage: userMessage,
            chatbotResponse: chatbotResponse,
        },
        dataType: 'json',
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken },
        success: function () {
            console.log('Conversation saved to the database');
        },
        error: function () {
            console.error('An error occurred while saving the conversation to the database.');
        },
    });
}