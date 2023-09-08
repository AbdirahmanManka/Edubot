from django.shortcuts import render
from django.http import JsonResponse
from .models import Conversation
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def home(request):
    if request.method == 'POST':
        user_message = request.POST.get('user_message')
        user_email = request.POST.get('user_email')
        Conversation.objects.create(user_email=user_email, message=user_message
        bot_response = generate_bot_response(user_message)
        Conversation.objects.create(user_email='', message=bot_response)
        return JsonResponse({'bot_response': bot_response})
    return render(request, 'home.html')

def generate_bot_response(user_message):
    user_message = user_message.lower()  
    responses = {
        'hello': 'Hello! How can I assist you today?',
        'accounts': 'Sure! Please enter your admission number.',
        'programs': 'Here are the available programs: Program 1, Program 2, Program 3. Please choose one.',
        'other issue': "I'm sorry, I can't assist with that at the moment. Please choose from: Accounts, Programs, Other Issue.",
        'goodbye': 'Thank you for chatting with us. Have a great day!',
    }

    for keyword, response in responses.items():
        if keyword in user_message:
            return response
    return "I'm sorry, I didn't understand your message. Please choose from: Accounts, Programs, Other Issue, Goodbye."

@csrf_exempt 
def chatbot(request):
    if request.method == 'POST':
        user_message = request.POST.get('user_message')
        bot_response = generate_bot_response(user_message)
        return JsonResponse({'bot_response': bot_response})
    return JsonResponse({})
