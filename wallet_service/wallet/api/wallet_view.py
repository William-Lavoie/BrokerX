import json
import logging
from decimal import ROUND_HALF_UP, Decimal

import jwt
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from wallet.adapters.django_wallet_repository import DjangoWalletRepository
from wallet.adapters.django_withdrawal_repository import DjangoWithdrawalRepository
from wallet.adapters.mock_payment_service_repository import MockPaymentServiceRepository
from wallet.services.add_funds_to_wallet_use_case import AddFundsToWalletUseCase

logger = logging.getLogger("wallet")
SECRET_KEY = "gq35rgaerFW53T45GQ345FAdasfawf24k7iy"


class WalletView(APIView):
    permission_classes = [AllowAny]

    def put(self, request):
        token = request.headers.get("Authorization").split(" ")[1]

        try:
            uuid = jwt.decode(token, SECRET_KEY, algorithms=["HS256"]).get("uuid")
            email = jwt.decode(token, SECRET_KEY, algorithms=["HS256"]).get("email")
            logger.error(f"request : {request.__dict__}")
            data = json.loads(request.body)

            amount = Decimal(data.get("amount")).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            idempotency_key = request.headers.get("Idempotency-Key")

            use_case = AddFundsToWalletUseCase(
                MockPaymentServiceRepository(),
                DjangoWalletRepository(),
                DjangoWithdrawalRepository(),
            )

            result = use_case.execute(uuid, email, amount, idempotency_key)

            return JsonResponse(data=result.to_dict(), status=result.code)

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            return JsonResponse({"error": "An unexpected error occurred."}, status=500)

    def get(self, request):
        token = request.headers.get("Authorization").split(" ")[1]

        try:
            uuid = jwt.decode(token, SECRET_KEY, algorithms=["HS256"]).get("uuid")
            logger.info(f"Extracted UUID from token: {uuid}")

            use_case = AddFundsToWalletUseCase(
                MockPaymentServiceRepository(),
                DjangoWalletRepository(),
                DjangoWithdrawalRepository(),
            )

            result = use_case.get_balance(uuid)

            return JsonResponse(data=result.to_dict(), status=result.code)

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return JsonResponse({"error": "An unexpected error occurred."}, status=500)
