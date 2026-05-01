from django.db import models

# Create your models here.
class Answer(models.Model):
    answer = models.TextField()
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

class Question(models.Model):
    question = models.TextField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

class Quiz(models.Model):
    title = models.CharField(max_length=100)

class Submission(models.Model):
    title = models.CharField(max_length=100)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def add_question(self, question, answers):
        self.quiz.questions.add(question)
        self.quiz.questions[len(self.quiz.questions)-1].add(answers)
        self.save()