from django.db import models
from django.contrib.auth.models import User  # Імпортуємо стандартну модель користувача


class Quiz(models.Model):
    title = models.CharField(max_length=100)
    # Додаємо зв'язок з користувачем. Якщо користувача видалять, його квізи теж видаляться.
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')

    def __str__(self):
        return self.title


# Моделі Question та Answer залишаються без змін
class Question(models.Model):
    question = models.TextField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.question


class Answer(models.Model):
    answer = models.TextField()
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer


class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()  # Кількість правильних відповідей
    total_questions = models.IntegerField()  # Всього питань у тесті
    date_taken = models.DateTimeField(auto_now_add=True)  # Дата і час проходження

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}: {self.score}/{self.total_questions}"


"""
class QuestionSubmission(models.Model): # добавление вопросов к квизу
    title = models.CharField(max_length=100)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return (self.title, self.quiz)

    def add_question(self, question, answers):
        self.quiz.questions.add(question)
        self.quiz.questions[len(self.quiz.questions)-1].add(answers)
        self.save()

class QuizSubmission(models.Model): # добавление квизов
    title = models.CharField(max_length=100)
    quiz = Quiz()

    def __str__(self):
        return (self.title, self.quiz)

    def add_question(self, question, answers):
        self.quiz.questions.add(question)
        self.quiz.questions[len(self.quiz.questions)-1].add(answers)
        self.save()"""
