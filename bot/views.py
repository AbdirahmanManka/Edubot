import json
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import Student
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse


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
    return redirect('custom_login')  # Redirect to the custom_login page after logout

def chatbot_response(request):
    user_message = request.GET.get('userMessage')  # Get the user's message from the request
    print(user_message)
    # Process the user_message and generate a response
    # You can use a Python function or library for chatbot logic
    chatbot_response = generate_chatbot_response(user_message)
    return JsonResponse({'response': chatbot_response})