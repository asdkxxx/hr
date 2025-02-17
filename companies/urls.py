from django.urls import path
from .views import CompanyRegistrationView, CompanyLoginView

urlpatterns = [
    # Теперь POST /api/companies/register
    path('register/', CompanyRegistrationView.as_view(), name='company-register'),
    # Теперь POST /api/companies/login
    path('login/', CompanyLoginView.as_view(), name='company-login'),
]
