from django.db import models
from django.utils import timezone
from login_registration.models import CollegeRegistration, User, Profile
# Create your models here.


class PaymentCredentials(models.Model):
    secret_key = models.TextField()
    secret_id = models.TextField()

    def __str__(self) -> str:
        return self.secret_key


class PackageSetting(models.Model):
    price_per_student = models.PositiveIntegerField()


class Invoice(models.Model):
    college = models.ForeignKey(CollegeRegistration, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    student_limit = models.PositiveIntegerField()
    paid_on = models.DateTimeField(default=timezone.now)
    expiry = models.DateTimeField(null=True)
