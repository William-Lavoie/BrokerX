import json
import logging

from client.adapters.django_client_repository import DjangoClientRepository
from django.http import JsonResponse
from otp.adapters.email_otp_repository import EmailOTPRepository
from otp.services.verify_passcode import VerifyPassCode
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

logger = logging.getLogger("django.server")


class OTPView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logger.error(request.body)
        logger.error(request.headers)
        data = json.loads(request.body)

        passcode = data["passcode"]

        use_case = VerifyPassCode(EmailOTPRepository(), DjangoClientRepository())
        result = use_case.execute(request.user.uuid, request.user.email, passcode)

        return JsonResponse(data=result.to_dict(), status=result.code)

    def put(self, request):
        use_case = VerifyPassCode(EmailOTPRepository(), DjangoClientRepository())
        result = use_case.generate_passcode(request.user.uuid, request.user.email)

        return JsonResponse(data=result.to_dict(), status=result.code)
