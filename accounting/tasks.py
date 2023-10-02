from celery import shared_task, Celery
from login_registration.models import CollegeRegistration, Profile
app = Celery()

@shared_task
def disable_student_group(college_email):
    college_object = CollegeRegistration.objects.get(college_email=college_email)
    Profile.objects.filter(college=college_object, user__groups__name='student').update(login_allow=False)
