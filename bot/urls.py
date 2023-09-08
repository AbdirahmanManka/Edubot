from django.urls import path 
from . import views
from django.contrib.auth.views import LogoutView, LoginView
# from .forms import UserLoginForm
# from .views import signup
# from django.conf.urls import url


urlpatterns=[
    path('', views.home, name='home'),
    path('chatbot/', views.chatbot, name='chatbot'),
    
]