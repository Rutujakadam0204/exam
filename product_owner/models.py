from django.db import models


class Exam(models.Model):
    name = models.CharField(max_length=1000, blank=True)


class Question(models.Model):
    experiment = models.IntegerField(null=True, blank=True)
    text = models.CharField(max_length=100000, blank=True)
    question_display_type = models.CharField(max_length=100, blank=True)
    quest_image = models.FileField(upload_to="question/image/", blank=True)
