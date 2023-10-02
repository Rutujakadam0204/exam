from django.contrib.auth.forms import UserCreationForm
from .models import User
# from rest_framework.serializers import U


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']