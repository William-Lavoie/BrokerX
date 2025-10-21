import json
import logging

from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from ..adapters.django_client_repository import DjangoClientRepository
from ..adapters.email_otp_repository import EmailOTPRepository
from ..services.create_account_use_case.verify_passcode import VerifyPassCode

logger = logging.getLogger(__name__)


class OTPView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = json.loads(request.body)

        passcode = data["passcode"]

        use_case = VerifyPassCode(EmailOTPRepository(), DjangoClientRepository())
        result = use_case.execute(request.user.email, passcode)

        return JsonResponse(data=result.to_dict(), status=result.code)

    def put(self, request):
        use_case = VerifyPassCode(EmailOTPRepository(), DjangoClientRepository())
        result = use_case.generate_passcode(request.user.email)

        return JsonResponse(data=result.to_dict(), status=result.code)
