# companies/models.py
from django.db import models

# Используем JSONField (Django 3.1+)
try:
    from django.db.models import JSONField
except ImportError:
    from django.contrib.postgres.fields import JSONField

class Company(models.Model):
    full_name = models.CharField(max_length=255)
    password = models.CharField(max_length=128)  # На практике храните хэш пароля!
    phone_number = models.CharField(max_length=20, unique=True)
    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    company_description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    logo_hr = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.company_name

    def get_username(self):
        return self.phone_number

class Vacancy(models.Model):
    job_title = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    hiring_plan = models.IntegerField()
    work_format = models.CharField(max_length=100)
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)
    experience = models.CharField(max_length=255)
    required_skills = JSONField(default=list, blank=True)
    job_description = models.TextField()
    responsibilities = JSONField(default=list, blank=True)
    requirements = JSONField(default=list, blank=True)
    conditions = JSONField(default=list, blank=True)

    def __str__(self):
        return self.job_title

# Новая модель для откликов кандидатов
class Response(models.Model):
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    experience = models.CharField(max_length=255)
    photo = models.URLField(blank=True, null=True)
    # При желании можно добавить связи с Vacancy или Candidate

    def __str__(self):
        return self.full_name
