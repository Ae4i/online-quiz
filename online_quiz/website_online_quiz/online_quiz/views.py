from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views.generic import CreateView


# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'templates/login.html'

class CustomLogoutView(LogoutView):
    next_page = 'templates:login'

class RegisterView(CreateView):
    template_name = 'templates/register.html'