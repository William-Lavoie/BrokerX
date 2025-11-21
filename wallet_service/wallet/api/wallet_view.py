import json
import logging
from decimal import ROUND_HALF_UP, Decimal

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from wallet.adapters.django_wallet_repository import DjangoWalletRepository
from wallet.adapters.django_withdrawal_repository import \
    DjangoWithdrawalRepository
from wallet.adapters.mock_payment_service_repository import \
    MockPaymentServiceRepository
from wallet.services.add_funds_to_wallet_use_case import \
    AddFundsToWalletUseCase

logger = logging.getLogger("wallet")


@method_decorator(csrf_exempt, name="dispatch")
class WalletView(APIView):
    permission_classes = [AllowAny]

    def put(self, request):
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

        uuid = "7a82a0d7197b422c9f884fab0975359a"
        email = "rocks@xebec.com"

        result = use_case.execute(uuid, email, amount, idempotency_key)

        return JsonResponse(data=result.to_dict(), status=result.code)

    def get(self, request):
        logger.error(request.headers)

        use_case = AddFundsToWalletUseCase(
            MockPaymentServiceRepository(),
            DjangoWalletRepository(),
            DjangoWithdrawalRepository(),
        )

        uuid = "7a82a0d7197b422c9f884fab0975359a"
        result = use_case.get_balance(uuid)

        return JsonResponse(data=result.to_dict(), status=result.code)
