from django.urls import path

from . import admin
from .views import *

app_name = "education"

urlpatterns = [
    path('/', QuizView.as_view(), name='quiz'),
]