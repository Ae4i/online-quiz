'''
from rest_framework import serializers
from .models import Quiz
class QuizSerializer(serializers.ModelSerializer):
 class Meta:
  model = Poll
  fields = ["id"]
'''