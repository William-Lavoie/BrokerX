import json
import logging
from dataclasses import asdict

from client.adapters.django_client_repository import DjangoClientRepository
from django.http import JsonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

# from client.services.create_account_use_case.create_client import CreateClientUseCase

logger = logging.getLogger(__name__)


class ClientView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def post(self, request):
        data = json.loads(request.body)

        first_name = data["first_name"]
        last_name = data["last_name"]
        address = data["address"]
        birth_date = data["date_of_birth"]
        email = data["email"]
        phone_number = data["phone_number"]
        password = data["password"]

        use_case = CreateClientUseCase(DjangoClientRepository(), EmailOTPRepository())

        result = use_case.execute(client_command)
        return JsonResponse(result.to_dict(), status=result.code)

    def get(self, request):
        use_case = CreateClientUseCase(DjangoClientRepository(), EmailOTPRepository())
        result = use_case.get_client_info(request.user.email)
        logger.error(result.to_dict())
        return JsonResponse(result.to_dict())
