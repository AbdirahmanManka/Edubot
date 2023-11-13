import json
import os
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import Student
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from difflib import get_close_matches
from .models import Conversation, UserProfile
from django.db import IntegrityError

def home(request):
    return render(request, 'home.html')

def login(request):
    if request.method == 'POST':
        user_email = request.POST.get('user_email')
        admission_number = request.POST.get('admission_number')

        user_profile = UserProfile.objects.filter(user_email=user_email, admission_number=admission_number).first()

        if user_profile is not None:
            # Use authenticate to check credentials
            user = authenticate(request, user_email=user_email, admission_number=admission_number)
            print(user)
            if user is not None:
                messages.error(request, 'Invalid login credentials.')  
            else:
                return redirect('home')
        else:
            messages.error(request, 'User not found. Please check your credentials.')

    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        user_email = request.POST.get('user_email')
        admission_number = request.POST.get('admission_number')

        try:
            UserProfile.objects.create(user_email=user_email, admission_number=admission_number)
            messages.success(request, 'Signup successful. You can now login.')
            return redirect('home')  
        except IntegrityError as e:
            messages.error(request, 'User with this email already exists. Please use a different email.')

    return render(request, 'signup.html')

def user_logout(request):
    logout(request)
    return redirect('login')  

def chatbot_response(request):
    user_message = request.POST.get('userMessage')  
    chatbot_response = generate_chatbot_response(user_message)
    return JsonResponse({'response': chatbot_response})

def load_knowledge_base(file_name):
    data_dir = os.path.join(os.path.dirname(__file__), 'data')  # 'data' folder
    file_path = os.path.join(data_dir, file_name)
    with open(file_path, 'r') as file:
        knowledge_base = json.load(file)
    return knowledge_base

def chatbot_response(request):
    user_message = request.POST.get('userMessage')  
    chatbot_response = generate_chatbot_response(user_message)
    return JsonResponse({'response': chatbot_response})

def generate_chatbot_response(user_message):
    user_message = user_message.lower()

    # Load the knowledge base
    knowledge_base = load_knowledge_base('knowledge_base.json')

    # Extract the list of questions from the knowledge base
    questions = [q["question"].lower() for q in knowledge_base["questions"]]

    # Find the best match for the user's query
    best_match = find_best_match(user_message, questions)

    if best_match:
        # If there's a match, retrieve the answer from the knowledge base
        answer = get_answer_for_question(best_match, knowledge_base)
        return answer
    else:
        # If there's no match, provide a default response
        return "I'm sorry, I couldn't understand your request."

def find_best_match(user_question, questions):
    # Use your existing get_close_matches function
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question, knowledge_base):
    for q in knowledge_base["questions"]:
        if q["question"].lower() == question:
            return q["answer"]
        
def save_conversation(request):
    if request.method == 'POST':
        user_message = request.POST.get('userMessage')
        chatbot_response = request.POST.get('chatbotResponse')
        
        Conversation.objects.create(
            user_email=request.session.get('user_email'),  # Assuming you have the user's email in the session
            message=user_message,
            bot_response=chatbot_response  # Save the bot's response in the bot_response field
        )
    
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})