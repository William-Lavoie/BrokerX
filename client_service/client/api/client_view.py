import json
import logging

from client.adapters.django_client_repository import DjangoClientRepository
from client.services.create_client import CreateClientUseCase
from django.http import JsonResponse
from otp.adapters.email_otp_repository import EmailOTPRepository
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from client_service.serializers import MyTokenObtainPairSerializer

logger = logging.getLogger("django.server")


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ClientView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def post(self, request):
        logger.error(request.body)
        logger.error(request.headers)
        data = request.data

        first_name = data["first_name"]
        last_name = data["last_name"]
        address = data["address"]
        birth_date = data["date_of_birth"]
        email = data["email"]
        phone_number = data["phone_number"]
        password = data["password"]

        use_case = CreateClientUseCase(DjangoClientRepository(), EmailOTPRepository())

        result = use_case.execute(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            email=email,
            phone_number=phone_number,
            address=address,
            password=password,
        )
        return JsonResponse(result.to_dict(), status=result.code)

    def get(self, request):
        logger.error(request.body)
        logger.error(request.headers)
        use_case = CreateClientUseCase(DjangoClientRepository(), EmailOTPRepository())
        result = use_case.get_client_info(request.user.email)
        logger.error(request.user.uuid)
        return JsonResponse(result.to_dict())
