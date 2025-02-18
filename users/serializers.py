# users/serializers.py
from rest_framework import serializers
from .models import UserRegistration, UserResume

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRegistration
        fields = [
            'id',
            'full_name',
            'password',
            'phone_number',
            'created_at',
            'user_pic',
        ]
        read_only_fields = ['created_at']

class UserResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResume
        fields = [
            'id',
            'full_name',
            'position',
            'specialization',
            'work_format',
            'ready_for_business_trips',
            'expected_salary',
            'experience',
            'photo',
            'skills',
            'about',
            'languages',
            'education',
        ]
