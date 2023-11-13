from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),  
    path('chatbot_response/', views.chatbot_response, name='chatbot_response'),
    path('save_conversation/', views.save_conversation, name='save_conversation'),
]
