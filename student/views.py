import json
from django.contrib import messages
from django.shortcuts import render, redirect
from product_owner.models import Question, Exam
from rest_framework.views import APIView
from rest_framework.response import Response
from . models import GivenExam, Answer
from django.db import transaction
from login_registration.models import Profile
from datetime import datetime
from django.http import HttpResponseRedirect

class MyExam(APIView):
    def get(self, request, pk):
        quest = Answer.objects.filter(exam_details__id=pk)
        data = {'quest': quest, 'exam_id': pk}
        return render(request, 'exam_page.html', data)


class MyExamAnswer(APIView):
    def get(self, request, pk):
        if not Answer.objects.filter(id=pk, exam_details__exam_submitted=True).exists():
            Answer.objects.filter(id=pk).update(text=request.GET['answer'])
            return Response({'msg':'Answer submitted successfully !!!'})
        else:
            return Response({'msg':'Answer already recorded'})


class ExamDetails(APIView):
    def get(self, request):
        data = {'exam_type': Exam.objects.all()}
        return render(request, 'exam_details.html', data)

    @transaction.atomic()
    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        if GivenExam.objects.filter(student=request.user, exam_type=Exam.objects.get(id=int(request.data['exam_type']))).exists():
            messages.success(request, 'This student already gave the selected exam.') 
            data = {'exam_type': Exam.objects.all()}
            return render(request, 'exam_details.html', data)
        else:    
            a = GivenExam.objects.create(
                                college=profile.college,
                                exam_type=Exam.objects.get(id=int(request.data['exam_type'])),
                                student=request.user,
                                exam_date=request.data['exam_date'],
                                from_exp=request.data['from_exp'],
                                to_exp=request.data['to_exp'],
                                student_roll=request.data['student_roll']
                                )

            exp = [i for i in range(int(request.data['from_exp']), int(request.data['to_exp'])+1)]
            values = Question.objects.filter(experiment__in=exp).values('id').order_by('?')[:20]
            print(values)
            # a list of unsaved Entry model instances
            my_list = [Answer(
                            exam_details=GivenExam.objects.get(id=a.id),
                            question=Question.objects.get(id=val['id'])
                    ) for val in values]
            Answer.objects.bulk_create(my_list)
            return redirect(f'/student/exam/{a.id}')


class ExamResult(APIView):

    def get(self, request, pk):
        exam = GivenExam.objects.get(id=pk)
        exam.exam_submitted = True
        exam.save()
        return render(request, 'result.html', {'exam_id':pk})

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from fpdf import FPDF, HTMLMixin
from django.core.files.base import File
import PyPDF2
import os

def some_view(request, pk):
    exam = GivenExam.objects.get(id=pk)
    student_name = exam.student.first_name+' '+exam.student.last_name
    student_roll_number = exam.student_roll
    exam_type = exam.exam_type.name
    date = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M')

    if exam.answer_pdf_file:
        pass
    else:
        answers = Answer.objects.filter(exam_details__id=pk)
        text = ''
        for answer in answers:
            text += "<b>Question</b> : <br>"+answer.question.text+"<br><b>Answer</b> : <br>"+answer.text+"<br><br>"
        pdf_name = 'exam_'+pk+'.pdf'
        class MyPdf(FPDF, HTMLMixin):
            pass
        pdf = MyPdf()
        pdf.add_page()
        # pdf.add_font('DejaVu', '', 'static/font/DejaVuSansCondensed.ttf', uni=True)
        # pdf.set_font('DejaVu', '', 14)
        pdf.write_html("Student :")
        pdf.write_html(student_name+"<br>")
        pdf.write_html("Roll number : "+student_roll_number+"<br>")
        pdf.write_html("Exam type : "+exam_type+"<br>")
        pdf.write_html("Date : "+date+"<br><br><br>")
        pdf.write_html(text)
        file_output = pdf.output(pdf_name, 'F')
        # pdf.close()
        pdfFileObj = open(pdf_name, 'rb')
        pdfReader = PyPDF2.PdfReader(pdfFileObj)
        file_output = File(pdfFileObj)
        pageObj = pdfReader.pages[0]
        exam.answer_pdf_file.save(pdf_name, file_output)
        os.remove(pdf_name)
    return FileResponse(exam.answer_pdf_file.open(), as_attachment=True)


# showing page of exams and submitted answers details (pdf file) to staff only
class SubmittedExamDetails(APIView):
    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        data = {'given_exams': GivenExam.objects.filter(college=profile.college)}
        return render(request, 'given_exam_details.html', data)


def deleteExamDetails(request, pk):
    GivenExam.objects.filter(id=pk).delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
