from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from website_online_quiz.online_quiz.mixins import UserIsOwnerMixin
from website_online_quiz.online_quiz.models import *

# Create your views here.

class CustomLoginView(LoginView): # войти в аккаунт
    template_name = 'templates/login.html'
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView): # выйти с аккаунта
    next_page = 'templates:login'

class RegisterView(CreateView): # создать аккаунт
    template_name = 'templates/register.html'
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save()
        login = self.request.user
        return redirect(reverse_lazy('tasks:login'))


class QuizView(CreateView): # вьюшка для просмотра квиза
    template_name = 'templates/base.html'

class SubmitQuestionView(UserIsOwnerMixin, LoginRequiredMixin, CreateView): # вьюшка для изменения квиза
    template_name = 'templates/submit_question.html'
    success_url = reverse_lazy('templates:base')

class SubmitQuizView(UserIsOwnerMixin, LoginRequiredMixin, CreateView): # вьюшка для добавления квиза
    template_name = 'templates/submit_quiz.html'
    success_url = reverse_lazy('templates:base')