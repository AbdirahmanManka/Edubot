from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),  # Login page
    path('logout/', views.user_logout, name='logout'),  # Logout view
    # path('', views.home, name='home'),  # Home page
    path('check_email/', views.check_email, name='check_email'),  # Check email in the database
    path('handle_responses/', views.handle_responses, name='handle_responses'),  # Handle responses
]
