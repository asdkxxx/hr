from django.urls import path
from .views import UserRegistrationView, UserLoginView

urlpatterns = [
    # Регистрация пользователя: POST /api/user/register
    path('register', UserRegistrationView.as_view(), name='user-register'),
    # Логин пользователя: POST /api/user/login
    path('login', UserLoginView.as_view(), name='user-login'),
]
