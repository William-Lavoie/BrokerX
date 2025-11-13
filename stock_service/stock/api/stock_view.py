import json
import logging

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from stock.adapters.django_stock_repository import DjangoStockRepository
from stock.services.get_stock_info import GetStockInfoUseCase

logger = logging.getLogger("stock")


@method_decorator(csrf_exempt, name="dispatch")
class StockView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        symbol = request.GET.get("symbol")

        use_case = GetStockInfoUseCase(stock_repository=DjangoStockRepository())

        result = use_case.get_top_of_book(symbol=symbol)

        return JsonResponse(data=result.to_dict(), status=result.code)
