from django.db import models

class UserRegistration(models.Model):
    full_name = models.CharField(max_length=255)
    password = models.CharField(max_length=128)  # не забудьте хэшировать в реальном проекте!
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    user_pic = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.full_name

    def get_username(self):
        return self.phone_number
