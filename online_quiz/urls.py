from django.urls import path
from .views import *

app_name = "online_quiz"

urlpatterns = [
    path("", QuizListView.as_view(), name='quiz_list'),

    # Посилання для проходження квізу
    path("quiz/<int:pk>/pass/", PassQuizView.as_view(), name='pass_quiz'),

    # Особистий профіль та детальний перегляд для автора
    path("profile/", ProfileView.as_view(), name='profile'),
    path("quiz/<int:pk>/detail/", QuizDetailView.as_view(), name='quiz_detail'),

    # Створення
    path("add-quiz/", SubmitQuizView.as_view(), name='add_quiz'),
    path("add-question/", SubmitQuestionView.as_view(), name='add_question'),

    # Авторизація
    path("login/", CustomLoginView.as_view(), name='login'),
    path("logout/", CustomLogoutView.as_view(), name='logout'),
    path("register/", RegisterView.as_view(), name='register'),
]