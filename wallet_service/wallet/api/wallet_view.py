import json
import logging
from decimal import ROUND_HALF_UP, Decimal

from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from ..adapters.django_client_repository import DjangoClientRepository
from ..adapters.django_transaction_repository import DjangoTransactionRepository
from ..adapters.django_wallet_repository import DjangoWalletRepository
from ..adapters.mock_payment_service_repository import MockPaymentServiceRepository
from ..services.add_funds_to_wallet_use_case import AddFundsToWalletUseCase

logger = logging.getLogger(__name__)


class WalletView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = json.loads(request.body)

        amount = Decimal(data.get("amount")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        idempotency_key = request.headers.get("Idempotency-Key")

        use_case = AddFundsToWalletUseCase(
            DjangoClientRepository(),
            MockPaymentServiceRepository(),
            DjangoWalletRepository(),
            DjangoTransactionRepository(),
        )

        result = use_case.execute(request.user.email, amount, idempotency_key)

        return JsonResponse(data=result.to_dict(), status=result.code)

    def get(self, request):

        use_case = AddFundsToWalletUseCase(
            DjangoClientRepository(),
            MockPaymentServiceRepository(),
            DjangoWalletRepository(),
            DjangoTransactionRepository(),
        )

        result = use_case.get_balance(request.user.email)

        return JsonResponse(data=result.to_dict(), status=result.code)
