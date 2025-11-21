import json
import logging
from decimal import Decimal

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from stock.adapters.django_stock_repository import DjangoStockRepository
from stock.services.update_top_of_book import UpdateTopOfBookUseCase

logger = logging.getLogger("stock")


@method_decorator(csrf_exempt, name="dispatch")
class TopOfBookView(APIView):
    permission_classes = [AllowAny]

    def put(self, request):
        data = json.loads(request.body)

        symbol = data.get("symbol", None)
        quantity = data.get("quantity", None)
        price = data.get("price", None)
        order_type = data.get("order_type", None)

        if price is not None:
            price = Decimal(price)

        order_type = data.get("order_type", None)

        use_case = UpdateTopOfBookUseCase(stock_repository=DjangoStockRepository())

        result = use_case.update_top_of_book(
            symbol=symbol, quantity=quantity, type=order_type, price=price
        )

        return JsonResponse(data=result.to_dict(), status=result.code)
