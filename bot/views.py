import os
import json
import joblib
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from .models import Conversation
from .forms import CustomUserCreationForm
from difflib import get_close_matches
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

def home(request):
    return render(request, 'home.html')

def user_login(request):
    if request.method == 'POST':
        user_email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=user_email, password=password)

        if user is not None:
            auth_login(request, user)  
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials.')

    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Signup successful. You can now login.')
            return redirect('user_login')
        else:
            messages.error(request, 'An error occurred.')
            print(form.errors)
    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})

@require_POST
def chatbot_response(request):
    stop_words = ['exit', 'stop', 'thank you', 'etc']
    chat_history = []

    while True:
        user_message = request.POST.get('userMessage')

        # Check if user wants to exit
        if any(stop_word in user_message.lower() for stop_word in stop_words):
            response = "Goodbye!"
            chat_history.append({'user': user_message, 'chatbot': response})
            break

        # Generate chatbot response
        chatbot_response = generate_chatbot_response(user_message)

        # Store conversation history
        chat_history.append({'user': user_message, 'chatbot': chatbot_response})

        # Send the chatbot response
        return JsonResponse({'response': chatbot_response, 'history': chat_history})

@csrf_exempt
@require_POST
def save_conversation(request):
    if request.method == 'POST':
        user_message = request.POST.get('userMessage')
        chatbot_response = request.POST.get('chatbotResponse')

        Conversation.objects.create(
            message=user_message,
            bot_response=chatbot_response
        )
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})

def load_knowledge_base(file_name):
    data_dir = os.path.join(os.path.dirname(__file__), 'data')  
    file_path = os.path.join(data_dir, file_name)
    with open(file_path, 'r') as file:
        knowledge_base = json.load(file)
    return knowledge_base

knowledge_base = load_knowledge_base('knowledge_base.json')

vectorizer_path = os.path.join('bot', 'data', 'tfidf_vectorizer.joblib')
vectorizer = joblib.load(vectorizer_path)

classifier_path = os.path.join('bot', 'data', 'chatbot_model.joblib')
classifier = joblib.load(classifier_path)

def generate_chatbot_response(user_message):
    user_message = user_message.lower()

    questions = [q["question"].lower() for q in knowledge_base["questions"]]

    best_match = find_best_match(user_message, questions)

    if best_match:
        predicted_answer = classifier.predict(vectorizer.transform([best_match]))
        return predicted_answer[0]
    else:
        learn_keywords = ['learn', 'update', 'yes']
        if any(keyword in user_message.lower() for keyword in learn_keywords):
            return "Sure! Please provide more information to help me understand better."
        else:
            return "I'm sorry, I couldn't understand your request. If you want to help me learn, you can say 'learn' or 'update' and provide more information."

def find_best_match(user_question, questions):
    matches = get_close_matches(user_question, questions, n=10, cutoff=0.2)
    return matches[0] if matches else None