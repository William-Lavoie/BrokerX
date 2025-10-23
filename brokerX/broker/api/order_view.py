import json
import logging
from decimal import ROUND_HALF_UP, Decimal

from django.http import JsonResponse
from ..adapters.django_order_repository import DjangoOrderRepository
from ..adapters.django_stock_repository import DjangoStockRepository
from ..services.place_order import PlaceOrderUseCase
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from ..adapters.django_client_repository import DjangoClientRepository
from ..adapters.django_transaction_repository import DjangoTransactionRepository
from ..adapters.django_wallet_repository import DjangoWalletRepository
from ..adapters.mock_payment_service_repository import MockPaymentServiceRepository
from ..services.add_funds_to_wallet_use_case import AddFundsToWalletUseCase

logger = logging.getLogger(__name__)


class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = json.loads(request.body)

        direction = data.get("direction", "")
        limit = data.get("limit", None)
        quantity = int(data.get("quantity", 0))
        symbol = data.get("symbol", "")
        idempotency_key = request.headers.get("Idempotency-Key")

        use_case = PlaceOrderUseCase(
            DjangoClientRepository(),
            DjangoStockRepository(),
            DjangoOrderRepository(),
            DjangoWalletRepository(),
        )

        result = use_case.execute(
            email=request.user.email,
            direction=direction,
            limit=limit,
            quantity=quantity,
            symbol=symbol,
            idempotency_key=idempotency_key,
        )

        return JsonResponse(data=result.to_dict(), status=result.code)
    
    def get(self, request):

        use_case = PlaceOrderUseCase(
            DjangoClientRepository(),
            DjangoStockRepository(),
            DjangoOrderRepository(),
            DjangoWalletRepository(),
        )

        result = use_case.get_orders(request.user.email)
        return JsonResponse(data=result.to_dict(), status=result.code)
