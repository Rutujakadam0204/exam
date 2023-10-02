from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from django.db import transaction
from .models import Profile, User, CollegeRegistration
from django.contrib.auth.models import Group
from .serializers import CollegeSerializer, UserSerializer
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime
from django.contrib.auth import logout, login
from django.shortcuts import redirect, render
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.smtp import EmailBackend
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponseRedirect

# Create your views here.

# def send_payment_link(user):
#     User.objects.get(email=user.email)
#     encrypted_key = urlsafe_base64_encode(force_bytes(user.profile.college.college_email))
#     backend = EmailBackend(host=settings.EMAIL_HOST,
#                         port=settings.EMAIL_PORT,
#                         username=settings.EMAIL_HOST_USER,
#                         password=settings.EMAIL_HOST_PASSWORD,
#                         use_tls=settings.EMAIL_USE_TLS,fail_silently=False)
#     message = "http://localhost:8000/accounting/payment-after-invoice/"+ encrypted_key
#     msg = EmailMultiAlternatives(subject="Link for payment", body=message, from_email=settings.EMAIL_HOST_USER,to=[user.email], connection=backend)
#     msg.send()
#     return 0


def send_password_reset_link(user):
    User.objects.get(email=user.email)


class LoginView(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'login.html'

    @transaction.atomic()
    def get(self, request):
        data = {}
        return Response(data)
    
    @transaction.atomic()
    def post(self, request):
        data = {}
        if User.objects.filter(email=request.data['email']).exists():
            user = User.objects.get(email=request.data['email'])
            correct_password = check_password(request.data['password'], user.password)
            if correct_password:
                if user.profile.college.payment and user.profile.login_allow:
                    login(request, user)

                    data['redirect_url'] = '/student/exam-details'

                else:
                    if user.groups.filter(name='staff').exists():
                        # send_payment_link(user)
                        encrypted_key = urlsafe_base64_encode(force_bytes(user.profile.college.college_email))
                        data['redirect_url'] = '/accounting/payment-after-invoice/'+encrypted_key
                        data['message'] = "Make a payment first.You are being redirected to that page."
                    else:
                        data['redirect_url'] = '/login'
                        data['message'] = "Could not login, Login validity expired."
                
                return Response(data)
            else:
                data['message'] = "Wrong password."
                data['redirect_url'] = '/login'
                return Response(data)    
        else:
            data['message'] = "Email does not exists."
            data['redirect_url'] = '/login'
            return Response(data)


class LogoutView(APIView):
    @transaction.atomic()
    def get(self, request):
        logout(request)
        return redirect('/')


class UserProfileView(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'profile.html'

    @transaction.atomic()
    def get(self, request):
        data = {'user_profile': request.user.profile}
        return Response(data)


class CollegeRegistrationView(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'college_registration.html'
    
    @transaction.atomic()
    def get(self, request):
        data = {}
        return Response(data)
    
    @transaction.atomic()
    def post(self, request):
        data = {}
        user_serializer = UserSerializer(data=request.data)
        college_serializer = CollegeSerializer(data=request.data)
        if User.objects.filter(username=request.data['email']).exists():
            data['message'] = "error"
            data['error'] = "Email alreayd exists."
        else:
            if user_serializer.is_valid() and college_serializer.is_valid():
                password = make_password(request.data['password'])
                saved_college_serializer = college_serializer.save()
                print(saved_college_serializer)
                saved_user_serializer = user_serializer.save(password=password, username=request.data['email'])
                if Group.objects.filter(name='staff').exists():
                    group = Group.objects.get(name='staff')
                else:
                    group = Group.objects.create(name='staff')
                    group.save()
                group.user_set.add(saved_user_serializer)
                Profile.objects.create(college=saved_college_serializer, user=saved_user_serializer, login_allow=True, start_year=datetime.now().year, end_year=datetime.now().year+1)
                data['message'] = "success"
                data['redirect_url'] = "/login"
                data['success'] = "Successfully Registered"
            else:
                data['message'] = "error"
                data['error'] = {**user_serializer.errors, **college_serializer.errors}
        return Response(data)
    

class UserRegistrationView(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'user_registration.html'

    @transaction.atomic()
    def get(self, request):
        data = {
            'user_list': Profile.objects.filter(college=request.user.profile.college),
        }
        return Response(data)
    
    @transaction.atomic()
    def post(self, request):
        data = {}
        user_serializer = UserSerializer(data=request.data)
        if request.data['group_type'] == 'student' and request.data['roll_number'] != '':
            if Group.objects.filter(name='student').exists():
                group = Group.objects.get(name='student')
            else:
                group = Group.objects.create(name='student')
                group.save()
        elif request.data['group_type'] == 'staff':
            if Group.objects.filter(name='staff').exists():
                group = Group.objects.get(name='staff')
            else:
                group = Group.objects.create(name='staff')
                group.save()        
        else:
            data['message'] = "Roll number cannot be empty"
            return Response(data)
        
        profile_student_count = Profile.objects.filter(college=request.user.profile.college, login_allow=True, user__groups__name__contains=group.name).count()
        student_limit = request.user.profile.college.student_limit
        print(student_limit, profile_student_count)
        if not User.objects.filter(email=request.data['email']).exists():
            print(student_limit, profile_student_count)
            if student_limit > profile_student_count and request.data['group_type'] == 'student':
                if user_serializer.is_valid():
                    password = make_password(request.data['password'])
                    saved_user_serializer = user_serializer.save(password=password, username=request.data['email'])
                    group.user_set.add(saved_user_serializer)
                    profile = Profile.objects.create(college=request.user.profile.college, user=saved_user_serializer, start_year=datetime.now().year, end_year=datetime.now().year+1, login_allow=True)
                    profile.save()
                    if request.data['group_type'] == 'student':
                        profile.roll_number = request.data['roll_number']
                        profile.save()
                    data['message'] = "Successfully created user profile."
                else:
                    data['message'] = "Invalid data."
            elif request.data['group_type'] == 'staff':
                if user_serializer.is_valid():
                    password = make_password(request.data['password'])
                    saved_user_serializer = user_serializer.save(password=password, username=request.data['email'])
                    group.user_set.add(saved_user_serializer)
                    profile = Profile.objects.create(college=request.user.profile.college, user=saved_user_serializer, start_year=datetime.now().year, end_year=datetime.now().year+1, login_allow=True)
                    profile.save()
                    data['message'] = "Successfully created user profile."
                else:
                    data['message'] = "Invalid data."
            else:
                data['message'] = "Limit exceeded for Student registration."
        else:
            data['message'] = "User already is present"
        return Response(data)

def delete_user(request, pk):
    User.objects.filter(id=pk).delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    

def get_user_object(pk):
    return User.objects.get(id=pk)


class UserCrudApi(APIView):
    @transaction.atomic()
    def get(self, request, pk):
        user_object = get_user_object(pk)

        data = {
            'user_detail': user_object,
            'profile_detail': user_object.profile
        }
        return Response(data)
    
    @transaction.atomic()
    def put(self, request, pk):
        data = {}
        if request.data['action'] == 'allow':
            profile_student_count = Profile.objects.filter(college=request.user.profile.college, login_allow=True).count()
            student_limit = request.user.profile.college.student_limit
            if student_limit <=  profile_student_count:
                data['message'] = "Limit exceeded for user login"
            else:
                user_object = get_user_object(pk)
                user_object.profile.login_allow=True 
                user_object.profile.save() 
                data['message'] = "User login allowed for "+user_object.first_name+' '+user_object.last_name  
        else:
            user_object = get_user_object(pk)
            user_object.profile.login_allow=False
            user_object.profile.save()
            data['message'] = "Disable login allowed for "+user_object.first_name+' '+user_object.last_name

        return Response(data)
    
    @transaction.atomic()
    def delete(self, request, pk):
        data = {}
        user_object = get_user_object(pk)
        message = user_object.first_name + ' ' + user_object.last_name+ ' has been deleted.'
        user_object.delete()
        data['message'] = message
        return Response(data)


class HomeView(APIView):
    @transaction.atomic()
    def get(self, request):
        return render(request, 'home.html')
