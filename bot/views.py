import os
import json
import joblib
from difflib import get_close_matches
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from .models import Conversation
from .forms import CustomUserCreationForm
from sklearn.feature_extraction.text import TfidfVectorizer

def home(request):
    return render(request, 'home.html')

def login(request):
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
            return redirect('login')
        else:
            messages.error(request, 'An error occurred.')
            print(form.errors)
    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})

def chatbot_response(request):
    user_message = request.POST.get('userMessage')  
    chatbot_response = generate_chatbot_response(user_message)
    return JsonResponse({'response': chatbot_response})

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
        return "I'm sorry, I couldn't understand your request."

def find_best_match(user_question, questions):
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def save_conversation(request):
    if request.method == 'POST':
        user_message = request.POST.get('userMessage')
        chatbot_response = request.POST.get('chatbotResponse')
        
        Conversation.objects.create(
            user_email=request.session.get('user_email'), 
            message=user_message,
            bot_response=chatbot_response  
        )
    
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})