import json
import logging
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from order.adapters.django_order_repository import DjangoOrderRepository
from order.adapters.portfolio_service import PortfolioService
from order.adapters.stock_service import StockService
from order.adapters.wallet_service import WalletService
from order.services.place_order import PlaceOrderUseCase
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

logger = logging.getLogger("order")


@method_decorator(csrf_exempt, name="dispatch")
class OrderView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = json.loads(request.body)

        client_id = UUID("5a2753379b0a4db7baf166ab8946b511")
        symbol = data.get("symbol", "")
        order_type = data.get("order_type", "")
        order_style = data.get("order_style", "")
        order_duration = data.get("order_duration", "")
        price = data.get("price", None)

        if price is not None:
            price = Decimal(str(price))

        end_date = data.get("end_date", None)
        quantity = data.get("quantity", 0)

        if (
            not symbol
            or not order_type
            or not order_style
            or not order_duration
            or not quantity
        ):
            return JsonResponse(
                data={"message": "Missing required parameters.", "orders": []},
                status=400,
            )

        idempotency_key = request.headers.get("Idempotency-Key")

        use_case = PlaceOrderUseCase(
            order_repository=DjangoOrderRepository(),
            stock_repository=StockService(),
            wallet_repository=WalletService(),
            portfolio_repository=PortfolioService(),
        )

        result = use_case.execute(
            client_id=client_id,
            symbol=symbol,
            order_type=order_type,
            order_style=order_style,
            order_duration=order_duration,
            quantity=quantity,
            idempotency_key=UUID(idempotency_key),
            price=price if price else None,
            end_date=datetime.strptime(end_date, "%Y-%m-%d") if end_date else None,
        )

        return JsonResponse(data=result.to_dict(), status=result.code)

    def get(self, request):

        use_case = PlaceOrderUseCase(
            DjangoOrderRepository(),
        )

        client_id = UUID("5a2753379b0a4db7baf166ab8946b511")

        result = use_case.get_orders(client_id=client_id)
        return JsonResponse(data=result.to_dict(), status=result.code)

    def put(self, request):
        data = json.loads(request.body)

        client_id = UUID("5a2753379b0a4db7baf166ab8946b511")
        symbol = data.get("symbol", "")
        order_type = data.get("order_type", "")
        order_style = data.get("order_style", "")
        order_duration = data.get("order_duration", "")
        price = data.get("price", None)

        if price is not None:
            price = Decimal(str(price))

        end_date = data.get("end_date", None)
        quantity = data.get("quantity", 0)

        if (
            not symbol
            or not order_type
            or not order_style
            or not order_duration
            or not quantity
        ):
            return JsonResponse(
                data={"message": "Missing required parameters.", "orders": []},
                status=400,
            )

        idempotency_key = request.headers.get("Idempotency-Key")

        use_case = PlaceOrderUseCase(
            order_repository=DjangoOrderRepository(),
            stock_repository=StockService(),
            wallet_repository=WalletService(),
            portfolio_repository=PortfolioService(),
        )

        result = use_case.execute(
            client_id=client_id,
            symbol=symbol,
            order_type=order_type,
            order_style=order_style,
            order_duration=order_duration,
            quantity=quantity,
            idempotency_key=UUID(idempotency_key),
            price=price if price else None,
            end_date=datetime.strptime(end_date, "%Y-%m-%d") if end_date else None,
        )

        return JsonResponse(data=result.to_dict(), status=result.code)

    def delete(self, request):
        data = json.loads(request.body)
        order_id = UUID(data.get("order_id", ""))

        client_id = UUID("5a2753379b0a4db7baf166ab8946b511")

        use_case = PlaceOrderUseCase(
            order_repository=DjangoOrderRepository(), wallet_repository=WalletService()
        )

        result = use_case.delete_order(order_id=order_id, client_id=client_id)
        return JsonResponse(data=result.to_dict(), status=result.code)
