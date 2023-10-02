from django.shortcuts import render, redirect
from rest_framework.views import APIView
from . models import Question
from django.http import HttpResponseRedirect


class AddExam(APIView):
    def get(self, request):
        data = {
            'questions': Question.objects.all()
        }
        return render(request, 'crud_questions.html', data)

    def post(self, request):
        Question.objects.create(experiment=request.data['experiment'],
                                text=request.data['text'],
                                question_display_type=request.data['question_display_type'],
                                quest_image=request.data['quest_image'])
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class DeleteQuestion(APIView):
    def get(self, request, pk):
        Question.objects.filter(id=pk).delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
