from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),  
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('chatbot_response/', views.chatbot_response, name='chatbot_response'),
    path('save_conversation/', views.save_conversation, name='save_conversation'),
]
