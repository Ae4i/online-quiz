from django.contrib.auth import login  # Додано правильний імпорт для авторизації
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, ListView
from django.views import View

# Краще імпортувати конкретні моделі, а не використовувати '*'
from .models import Quiz, Question, Answer, QuizResult


# from .mixins import UserIsOwnerMixin  # Переконайтеся, що цей файл існує

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'  # Прибрано 'templates/'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('online_quiz:login')  # Виправлено неймспейс


class RegisterView(CreateView):
    template_name = 'accounts/register.html'
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save()
        # Правильна авторизація після реєстрації
        login(self.request, user)
        # Перенаправлення на головну сторінку додатку online_quiz
        return redirect(reverse_lazy('online_quiz:quiz_list'))


class QuizListView(ListView):
    model = Quiz  # Обов'язково вказуємо модель
    template_name = 'quiz/quiz_list.html'
    context_object_name = 'quizzes'  # Зручне ім'я для використання в HTML


# ДЕТАЛЬНИЙ ПЕРЕГЛЯД ДЛЯ АВТОРА (Тут видно правильні відповіді)
class QuizDetailView(LoginRequiredMixin, DetailView):
    model = Quiz
    template_name = 'quiz/view_quiz.html' # Ваш старий шаблон з правильними відповідями
    context_object_name = 'quiz'

    def dispatch(self, request, *args, **kwargs):
        # Перевірка: якщо користувач не є автором цього квізу, не пускаємо його сюди
        quiz = get_object_or_404(Quiz, pk=self.kwargs['pk'])
        if quiz.author != request.user:
            return redirect('online_quiz:quiz_list')
        return super().dispatch(request, *args, **kwargs)


# Для CreateView потрібно вказати модель та поля, які будуть у формі
class SubmitQuestionView(LoginRequiredMixin, CreateView):
    model = Question
    fields = ['question', 'quiz']
    template_name = 'quiz/submit_question.html'
    success_url = reverse_lazy('online_quiz:quiz_list')


# Автоматично робимо користувача автором
class SubmitQuizView(LoginRequiredMixin, CreateView):
    model = Quiz
    fields = ['title']
    template_name = 'quiz/submit_quiz.html'
    success_url = reverse_lazy('online_quiz:quiz_list')

    def form_valid(self, form):
        form.instance = form.save(commit=False)
        form.instance.author = self.request.user # Призначаємо автора
        form.instance.save()
        return redirect(self.success_url)


# ПРОХОДЖЕННЯ КВІЗУ (Для головної сторінки — правильні відповіді приховані)
class PassQuizView(View):

    # 1. Цей метод спрацьовує, коли користувач просто заходить на сторінку тесту
    def get(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        questions = quiz.question_set.all()
        return render(request, 'quiz/pass_quiz.html', {'quiz': quiz, 'questions': questions})

    # 2. Цей метод спрацьовує, коли користувач натискає кнопку і відправляє форму
    def post(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        questions = quiz.question_set.all()
        score = 0
        total = questions.count()

        # Обробка відповідей
        for question in questions:
            selected_answer_id = request.POST.get(f'question_{question.id}')
            if selected_answer_id:
                try:
                    answer = Answer.objects.get(id=selected_answer_id)
                    if answer.is_correct:
                        score += 1
                except Answer.DoesNotExist:
                    pass

        # Збереження результату в БД
        if request.user.is_authenticated:
            QuizResult.objects.create(
                user=request.user,
                quiz=quiz,
                score=score,
                total_questions=total
            )

        # Рендеримо шаблон з результатом успішного проходження
        return render(request, 'quiz/quiz_result.html', {'quiz': quiz, 'score': score, 'total': total})


# СТОРІНКА ПРОФІЛЮ (Показує лише квізи поточного юзера)
class ProfileView(LoginRequiredMixin, ListView):
    model = Quiz
    template_name = 'accounts/profile.html'
    context_object_name = 'user_quizzes'

    def get_queryset(self):
        # Фільтруємо квізи: беремо лише ті, де автор — це залогінений юзер
        return Quiz.objects.filter(author=self.request.user)


