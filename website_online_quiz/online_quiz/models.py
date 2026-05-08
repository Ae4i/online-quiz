from django.db import models

# Create your models here.
class Quiz(models.Model):
    title = models.CharField(max_length=100)

class Question(models.Model):
    question = models.TextField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

class Answer(models.Model):
    answer = models.TextField()
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

class QuestionSubmission(models.Model): # for submitting questions to a quiz
    title = models.CharField(max_length=100)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return (self.title, self.quiz)

    def add_question(self, question, answers):
        self.quiz.questions.add(question)
        self.quiz.questions[len(self.quiz.questions)-1].add(answers)
        self.save()

class QuizSubmission(models.Model): # for submitting questions to a quiz
    title = models.CharField(max_length=100)
    quiz = Quiz()

    def __str__(self):
        return (self.title, self.quiz)

    def add_question(self, question, answers):
        self.quiz.questions.add(question)
        self.quiz.questions[len(self.quiz.questions)-1].add(answers)
        self.save()