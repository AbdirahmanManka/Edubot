from django.shortcuts import render
from django.http import JsonResponse
from .models import Conversation  
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def home(request):
    if request.method == 'POST':
        user_message = request.POST.get('user_message')
        user_email = request.POST.get('user_email')

        # Save the user's message to the database
        Conversation.objects.create(user_email=user_email, message=user_message)

        # Process the user's message and generate a bot response
        bot_response = generate_bot_response(user_message)

        # Save the bot's response to the database
        Conversation.objects.create(user_email='', message=bot_response)

        # Return a JSON response with the bot's response
        return JsonResponse({'bot_response': bot_response})

    # If it's a GET request, render the home.html template
    return render(request, 'home.html')

# Implement the 'generate_bot_response' function here
def generate_bot_response(user_message):
    user_message = user_message.lower()  # Convert the user's message to lowercase for easier matching

    # Define predefined rules and responses
    responses = {
        'hello': 'Hello! How can I assist you today?',
        'accounts': 'Sure! Please enter your admission number.',
        'programs': 'Here are the available programs: Program 1, Program 2, Program 3. Please choose one.',
        'other issue': "I'm sorry, I can't assist with that at the moment. Please choose from: Accounts, Programs, Other Issue.",
        'goodbye': 'Thank you for chatting with us. Have a great day!',
    }

    # Check if the user's message matches any predefined rules
    for keyword, response in responses.items():
        if keyword in user_message:
            return response

    # If no matching rule is found, provide a default response
    return "I'm sorry, I didn't understand your message. Please choose from: Accounts, Programs, Other Issue, Goodbye."


@csrf_exempt  # Add this decorator to allow POST requests without CSRF tokens (for simplicity)
def chatbot(request):
    if request.method == 'POST':
        user_message = request.POST.get('user_message')

        # Process the user's message and generate a bot response
        bot_response = generate_bot_response(user_message)

        # Return a JSON response with the bot's response
        return JsonResponse({'bot_response': bot_response})

    # If it's not a POST request, return an empty response
    return JsonResponse({})
