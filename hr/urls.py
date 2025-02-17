from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="HR API",
        default_version='v1',
        description="Документация API для регистрации компаний и пользователей (JWT + Swagger)",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Переименовали 'api/hr/' → 'api/companies/'
    path('api/companies/', include('companies.urls')),

    # Для пользователей оставили как есть (или тоже переименуйте по аналогии)
    path('api/user/', include('users.urls')),

    # Swagger и Redoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # JSON или YAML схема
    path('swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
