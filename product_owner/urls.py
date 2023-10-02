from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from . views import AddExam, DeleteQuestion

urlpatterns = [
    path('home', login_required(AddExam.as_view())),
    path('delete-question/<int:pk>', login_required(DeleteQuestion.as_view())),
]
