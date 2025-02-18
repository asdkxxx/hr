# users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegistrationView, UserLoginView, UserRegistrationViewSet,
    UserResumeViewSet, JobSearchView
)

router = DefaultRouter()
router.register(r'profile', UserRegistrationViewSet, basename='user')
router.register(r'resume', UserResumeViewSet, basename='resume')

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    # Эндпоинт для поиска вакансий (работы) для юзера
    path('vacancy/', JobSearchView.as_view(), name='job-search'),
    path('', include(router.urls)),
]
