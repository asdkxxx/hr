from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

# Импортируем Swagger-утилиты
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import UserRegistration
from .serializers import UserRegistrationSerializer


class UserRegistrationView(generics.CreateAPIView):
    """
    Регистрация пользователя.
    """
    queryset = UserRegistration.objects.all()
    serializer_class = UserRegistrationSerializer

    @swagger_auto_schema(
        operation_summary="Регистрация пользователя",
        operation_description="Создаёт новую запись о пользователе на основе переданных данных (phone_number, password и т.д.).",
        responses={
            201: openapi.Response(
                description="Успешная регистрация",
                schema=UserRegistrationSerializer
            ),
            400: "Некорректные данные запроса"
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Переопределяем метод post, чтобы добавить декоратор Swagger.
        """
        return super().post(request, *args, **kwargs)


class UserLoginView(APIView):
    """
    Логин пользователя (получение JWT-токенов).
    """

    @swagger_auto_schema(
        operation_summary="Логин пользователя",
        operation_description="Авторизация по phone_number и password. Возвращает пару JWT-токенов (refresh и access).",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone_number': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Номер телефона пользователя'
                ),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Пароль'
                ),
            },
            required=['phone_number', 'password']
        ),
        responses={
            200: openapi.Response(
                description="Успешная авторизация",
                examples={
                    "application/json": {
                        "refresh": "string",
                        "access": "string"
                    }
                }
            ),
            400: "Неверные учётные данные или неполный запрос"
        }
    )
    def post(self, request):
        phone_number = request.data.get("phone_number")
        password = request.data.get("password")
        if not phone_number or not password:
            return Response(
                {"error": "phone_number и password обязательны."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = UserRegistration.objects.get(phone_number=phone_number)
        except UserRegistration.DoesNotExist:
            return Response(
                {"error": "Неверные учётные данные."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if user.password != password:
            return Response(
                {"error": "Неверные учётные данные."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Генерируем JWT-токены
        refresh = RefreshToken.for_user(user)
        refresh['type'] = 'user'
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })
