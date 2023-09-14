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
from .models import Conversation

def login(request):
    if request.method == 'POST':
        user_email = request.POST.get('user_email')
        admission_number = request.POST.get('admission_number')

        try:
            # Check if the user with provided email and admission number exists (case-insensitive)
            student = Student.objects.get(email__iexact=user_email, admission_number=admission_number)

            # Set a session variable to indicate that the user is logged in
            request.session['user_email'] = student.email  # Use the exact email from the database

            # messages.success(request, f"Welcome, {student.name}!")
            user = student.name
            return render(request, 'home.html', {'user': user}) # Redirect to the home page after successful login
        
        except Student.DoesNotExist:
            # If the student does not exist, show an error message
            messages.error(request, 'Invalid email or admission number. Please try again.')

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to the custom_login page after logout

def chatbot_response(request):
    user_message = request.POST.get('userMessage')  
    chatbot_response = generate_chatbot_response(user_message)
    return JsonResponse({'response': chatbot_response})

# Load the knowledge base from a JSON file
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
            message=user_message
        )
        
        Conversation.objects.create(
            user_email='bot@example.com',  # Use a placeholder email for the bot
            message=chatbot_response
        )
        
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})

