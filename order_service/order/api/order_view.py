import json
import logging

from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from ..adapters.django_order_repository import DjangoOrderRepository
from ..services.place_order import PlaceOrderUseCase

logger = logging.getLogger("order")


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
            DjangoOrderRepository(),
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
            DjangoOrderRepository(),
        )

        result = use_case.get_orders(request.user.email)
        return JsonResponse(data=result.to_dict(), status=result.code)
