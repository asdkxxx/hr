# companies/views.py
from rest_framework import generics, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response as DRFResponse
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Company, Vacancy, Response
from .serializers import (
    CompanyRegistrationSerializer,
    VacancySerializer,
    VacancySearchSerializer,
    ResponseSerializer
)

# Регистрация компании
class CompanyRegistrationView(generics.CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyRegistrationSerializer

    @swagger_auto_schema(
        operation_summary="Регистрация компании",
        operation_description="Создаёт новую компанию с переданными данными.",
        responses={201: CompanyRegistrationSerializer, 400: "Некорректные данные запроса"}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

# Логин компании (JWT)
class CompanyLoginView(APIView):
    @swagger_auto_schema(
        operation_summary="Логин компании",
        operation_description="Авторизация компании по phone_number и password. Возвращает JWT токены.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='Номер телефона'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Пароль'),
            },
            required=['phone_number', 'password']
        ),
        responses={200: openapi.Response(
            description="Успешная авторизация",
            examples={"application/json": {"refresh": "string", "access": "string"}}
        ), 400: "Неверные учетные данные"}
    )
    def post(self, request):
        phone_number = request.data.get("phone_number")
        password = request.data.get("password")
        if not phone_number or not password:
            return DRFResponse({"error": "phone_number и password обязательны."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            company = Company.objects.get(phone_number=phone_number)
        except Company.DoesNotExist:
            return DRFResponse({"error": "Неверные учетные данные."}, status=status.HTTP_400_BAD_REQUEST)
        if company.password != password:
            return DRFResponse({"error": "Неверные учетные данные."}, status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(company)
        refresh['type'] = 'company'
        return DRFResponse({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })

# CRUD для профиля компании
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanyRegistrationSerializer

# CRUD для вакансий
class VacancyViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer

# Новый эндпоинт для откликов кандидатов (только GET)
class ResponseListView(generics.ListAPIView):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer

    @swagger_auto_schema(
        operation_summary="Получить список откликов кандидатов",
        operation_description="Возвращает список кандидатов, которые откликнулись на вакансии.",
        responses={200: ResponseSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
