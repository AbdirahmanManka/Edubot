from django.urls import path 
from . import views
from django.contrib.auth.views import LogoutView, LoginView
# from .forms import UserLoginForm
# from .views import signup
# from django.conf.urls import url


urlpatterns=[
    path('', views.home, name='home'),
    # path("sign-up/", views.signup , name='signup'),
    # path("delete/", views.DeleteHistory, name='deleteChat'),
    # path("logout/", LogoutView.as_view(next_page='main'), name="logout"),
    # path("login/", LoginView.as_view(next_page='main', template_name="login.html", form_class = UserLoginForm), name="login"),
]