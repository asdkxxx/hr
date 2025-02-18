# companies/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CompanyRegistrationView, CompanyLoginView, CompanyViewSet,
    VacancyViewSet, ResponseListView
)

router = DefaultRouter()
router.register(r'profile', CompanyViewSet, basename='company')
router.register(r'vacancies', VacancyViewSet, basename='vacancy')

urlpatterns = [
    path('register/', CompanyRegistrationView.as_view(), name='company-register'),
    path('login/', CompanyLoginView.as_view(), name='company-login'),
    path('responses/', ResponseListView.as_view(), name='response-list'),
    path('', include(router.urls)),
]
