from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Student
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def login(request):
    if request.method == 'POST':
        user_email = request.POST.get('user_email')
        admission_number = request.POST.get('admission_number')

        # Check if the user with provided email and admission number exists
        try:
            student = Student.objects.get(email=user_email, admission_number=admission_number)
            # Set a session variable to indicate that the user is logged in
            request.session['user_email'] = user_email
            return redirect('home')  # Redirect to the home page after successful login
        except Student.DoesNotExist:
            messages.error(request, 'Invalid credentials. Please try again.')

    return render(request, 'login.html')

@login_required
def home(request):
    return render(request, 'home.html')

# Check Email in Database
@csrf_exempt  # Add CSRF exemption if needed
def check_email(request):
    if request.method == 'POST':
        user_email = request.POST.get('user_email')

        # Debugging: Print the email being queried
        print(f"Querying for email: {user_email}")

        # Check if the email exists in the database (case-insensitive)
        try:
            student = Student.objects.get(email__iexact=user_email)
            print(f"Email exists in the database: {student.name}")
            return JsonResponse({'result': 'Email exists', 'name': student.name})
        except Student.DoesNotExist:
            print("Email does not exist in the database")
            return JsonResponse({'result': 'Email does not exist'})

# Handle Responses
@csrf_exempt  # Add CSRF exemption if needed
def handle_responses(request):
    if request.method == 'POST':
        user_message = request.POST.get('user_message')

        # Process user message and generate a bot response (replace with your logic)
        bot_response = generate_bot_response(user_message)

        return JsonResponse({'bot_response': bot_response})
    return JsonResponse({})

# Implement your bot response logic here
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

from django.contrib.auth import logout

def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout
