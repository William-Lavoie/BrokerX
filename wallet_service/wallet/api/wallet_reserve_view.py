import json
import logging
from decimal import ROUND_HALF_UP, Decimal

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from wallet.adapters.django_wallet_repository import DjangoWalletRepository

logger = logging.getLogger("wallet")


@method_decorator(csrf_exempt, name="dispatch")
class WalletReserveView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = json.loads(request.body)

        amount = Decimal(data.get("amount")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        idempotency_key = request.headers.get("Idempotency-Key")
        client_id = data.get("client_id")

        use_case = ReserveFundsUseCase(
            DjangoWalletRepository(),
        )

        result = use_case.execute(client_id, amount, idempotency_key)

        return JsonResponse(data=result.to_dict(), status=result.code)
