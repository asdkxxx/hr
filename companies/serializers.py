from rest_framework import serializers
from .models import Company

class CompanyRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'id',
            'full_name',
            'password',
            'phone_number',
            'company_name',
            'industry',
            'company_description',
            'created_at',  # заполняется автоматически
            'logo_hr',
        ]
        read_only_fields = ['created_at']
