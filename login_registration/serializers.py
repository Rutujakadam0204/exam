from rest_framework import serializers
from .models import CollegeRegistration, User, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollegeRegistration
        exclude = ['register_on', 'payment']


# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['']
