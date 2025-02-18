# users/models.py
from django.db import models

# Используем JSONField (Django 3.1+)
try:
    from django.db.models import JSONField
except ImportError:
    from django.contrib.postgres.fields import JSONField

class UserRegistration(models.Model):
    full_name = models.CharField(max_length=255)
    password = models.CharField(max_length=128)  # Не храните пароли в открытом виде!
    phone_number = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user_pic = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.full_name

    def get_username(self):
        return self.phone_number

class UserResume(models.Model):
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    work_format = models.CharField(max_length=100)
    ready_for_business_trips = models.CharField(max_length=100)
    expected_salary = models.IntegerField()
    experience = models.CharField(max_length=255)
    photo = models.URLField(blank=True, null=True)
    skills = JSONField(default=list, blank=True)         # Пример: ["HTML", "CSS", "JavaScript"]
    about = models.TextField(blank=True)
    languages = JSONField(default=list, blank=True)      # Пример: [{"language": "English", "level": "B2"}]
    education = JSONField(default=list, blank=True)      # Пример: [{"univercity": "МГУ", "degree": "Бакалавр", "graduated": 2020}]

    def __str__(self):
        return f"{self.full_name} - {self.position}"
