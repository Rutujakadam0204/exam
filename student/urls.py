from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from . views import ExamDetails, MyExam, MyExamAnswer, some_view, ExamResult, SubmittedExamDetails, deleteExamDetails

urlpatterns = [
    path('exam-details', login_required(ExamDetails.as_view())),
    path('exam/<int:pk>', login_required(MyExam.as_view())),
    path('answer_questions_in_exam/<int:pk>', login_required(MyExamAnswer.as_view())),
    path('result/<pk>', login_required(ExamResult.as_view())),
    path('print/<pk>', some_view),
    path('exams-given-by-students',login_required(SubmittedExamDetails.as_view())),
    path('exams-given-by-students/<int:pk>',login_required(deleteExamDetails))

]
