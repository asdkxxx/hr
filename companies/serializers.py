# companies/serializers.py
from rest_framework import serializers
from .models import Company, Vacancy, Response

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
            'created_at',
            'logo_hr',
        ]
        read_only_fields = ['created_at']

class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = [
            'id',
            'job_title',
            'specialization',
            'city',
            'hiring_plan',
            'work_format',
            'salary_min',
            'salary_max',
            'experience',
            'required_skills',
            'job_description',
            'responsibilities',
            'requirements',
            'conditions',
        ]

# Для поиска вакансий у юзера — возвращаем только нужные поля
class VacancySearchSerializer(serializers.ModelSerializer):
    salary = serializers.SerializerMethodField()

    class Meta:
        model = Vacancy
        fields = ['job_title', 'specialization', 'salary']

    def get_salary(self, obj):
        return {"min": obj.salary_min}

# Для откликов кандидатов
class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ['full_name', 'position', 'experience', 'photo']
