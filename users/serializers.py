from rest_framework import serializers
from .models import UserRegistration

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRegistration
        fields = [
            'id',
            'full_name',
            'password',
            'phone_number',
            'created_at',  # заполняется автоматически
            'user_pic',
        ]
        read_only_fields = ['created_at']
