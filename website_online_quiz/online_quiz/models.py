from django.db import models

# Create your models here.
class Quiz(models.Model): # модель квиза
    title = models.CharField(max_length=100) # название квиза

class Question(models.Model): # модель вопроса
    question = models.TextField() # текст вопроса
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE) # связано к квизу много-к-одному

class Answer(models.Model): # модель ответа
    answer = models.TextField() # текст ответа
    is_correct = models.BooleanField(default=False) # правильный ли ответ
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # связано к вопросу много-к-одному
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