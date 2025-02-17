from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Company
from .serializers import CompanyRegistrationSerializer

class CompanyRegistrationView(generics.CreateAPIView):
    """
    Регистрация компании.
    """
    queryset = Company.objects.all()
    serializer_class = CompanyRegistrationSerializer

    @swagger_auto_schema(
        operation_summary="Регистрация компании",
        operation_description="Создаёт новую запись о компании на основе переданных данных.",
        responses={
            201: openapi.Response(
                description="Успешная регистрация",
                schema=CompanyRegistrationSerializer
            ),
            400: "Некорректные данные запроса"
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Переопределяем метод post, чтобы добавить документацию Swagger.
        """
        return super().post(request, *args, **kwargs)


class CompanyLoginView(APIView):
    """
    Логин компании (получение JWT-токенов).
    """

    @swagger_auto_schema(
        operation_summary="Логин компании",
        operation_description="Авторизация компании по phone_number и password. Возвращает JWT-токены (refresh и access).",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone_number': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Номер телефона компании'
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
            company = Company.objects.get(phone_number=phone_number)
        except Company.DoesNotExist:
            return Response(
                {"error": "Неверные учётные данные."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if company.password != password:
            return Response(
                {"error": "Неверные учётные данные."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Генерируем JWT-токены
        refresh = RefreshToken.for_user(company)
        refresh['type'] = 'company'
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })
