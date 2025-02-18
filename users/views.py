# users/views.py
from rest_framework import generics, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response as DRFResponse
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from companies.models import Vacancy  # для поиска вакансий
from companies.serializers import VacancySearchSerializer

from .models import UserRegistration, UserResume
from .serializers import UserRegistrationSerializer, UserResumeSerializer

# Регистрация пользователя
class UserRegistrationView(generics.CreateAPIView):
    queryset = UserRegistration.objects.all()
    serializer_class = UserRegistrationSerializer

    @swagger_auto_schema(
        operation_summary="Регистрация пользователя",
        operation_description="Создаёт нового пользователя с переданными данными.",
        responses={201: UserRegistrationSerializer, 400: "Некорректные данные запроса"}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

# Логин пользователя (JWT)
class UserLoginView(APIView):
    @swagger_auto_schema(
        operation_summary="Логин пользователя",
        operation_description="Авторизация пользователя по phone_number и password. Возвращает JWT токены.",
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
            user = UserRegistration.objects.get(phone_number=phone_number)
        except UserRegistration.DoesNotExist:
            return DRFResponse({"error": "Неверные учетные данные."}, status=status.HTTP_400_BAD_REQUEST)
        if user.password != password:
            return DRFResponse({"error": "Неверные учетные данные."}, status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(user)
        refresh['type'] = 'user'
        return DRFResponse({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })

# CRUD для профиля пользователя
class UserRegistrationViewSet(viewsets.ModelViewSet):
    queryset = UserRegistration.objects.all()
    serializer_class = UserRegistrationSerializer

# CRUD для резюме пользователя
class UserResumeViewSet(viewsets.ModelViewSet):
    queryset = UserResume.objects.all()
    serializer_class = UserResumeSerializer

# Новый эндпоинт для поиска вакансий (для юзера)
class JobSearchView(generics.ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySearchSerializer

    @swagger_auto_schema(
        operation_summary="Поиск работы (вакансии)",
        operation_description="Возвращает список вакансий с полями job_title, specialization и salary (min).",
        responses={200: VacancySearchSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
