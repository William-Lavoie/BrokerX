import json
import logging
from dataclasses import asdict

from django.http import JsonResponse
from rest_framework.views import APIView

from ..adapters.django_client_repository import DjangoClientRepository
from ..adapters.email_otp_repository import EmailOTPRepository
from ..services.commands.create_client_command import CreateClientCommand
from ..services.create_account_use_case.create_client import CreateClientUseCase

logger = logging.getLogger(__name__)


class ClientView(APIView):
    def post(self, request):
        data = json.loads(request.body)

        first_name = data["first_name"]
        last_name = data["last_name"]
        address = data["address"]
        birth_date = data["date_of_birth"]
        email = data["email"]
        phone_number = data["phone_number"]
        password = data["password"]

        client_command = CreateClientCommand(
            first_name=first_name,
            last_name=last_name,
            address=address,
            birth_date=birth_date,
            email=email,
            phone_number=phone_number,
            password=password,
        )

        use_case = CreateClientUseCase(DjangoClientRepository(), EmailOTPRepository())

        result = use_case.execute(client_command)
        return JsonResponse(asdict(result))
