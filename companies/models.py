from django.db import models

class Company(models.Model):
    full_name = models.CharField(max_length=255)  # имя контактного лица
    password = models.CharField(max_length=128)   # В реальном проекте храните пароль в хэшированном виде!
    phone_number = models.CharField(max_length=20)
    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    company_description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    logo_hr = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.company_name

    # Этот метод понадобится для генерации JWT через simplejwt
    def get_username(self):
        return self.phone_number
