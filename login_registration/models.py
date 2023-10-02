from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class CollegeRegistration(models.Model):
    college_name = models.CharField(max_length=100)
    register_on = models.DateTimeField(default=timezone.now)
    address = models.TextField()
    logo = models.ImageField(upload_to='logos', null=True)
    college_email = models.EmailField()
    mobile_number = models.PositiveBigIntegerField()
    payment = models.BooleanField(default=False)
    student_limit = models.IntegerField(default=0, null=True)

    def __str__(self) -> str:
        return str(self.college_name)


class Profile(models.Model):
    college = models.ForeignKey(CollegeRegistration, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    login_allow = models.BooleanField(default=False)
    start_year = models.IntegerField(null=True)
    end_year = models.IntegerField(null=True)
    roll_number = models.CharField(max_length=30, null=True)

    def __str__(self) -> str:
        return str(self.user.first_name)+" "+str(self.user.last_name)
