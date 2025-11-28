import json
import logging

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from portfolio.adapters.django_portfolio_repository import DjangoPortfolioRepository
from portfolio.services.reserve_holdings import ReserveHoldingsUseCase
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

logger = logging.getLogger("portfolio")


@method_decorator(csrf_exempt, name="dispatch")
class PortfolioReserveView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = json.loads(request.body)

        symbol = data.get("symbol")
        quantity = data.get("quantity")

        client_id = "5a2753379b0a4db7baf166ab8946b511"

        use_case = ReserveHoldingsUseCase(
            portfolio_repository=DjangoPortfolioRepository()
        )

        result = use_case.reserve_holdings(
            client_id=client_id, symbol=symbol, quantity=quantity
        )

        return JsonResponse(data=result.to_dict(), status=result.code)

    def put(self, request):
        data = json.loads(request.body)

        symbol = data.get("symbol")
        quantity = data.get("quantity")

        client_id = "5a2753379b0a4db7baf166ab8946b511"

        use_case = ReserveHoldingsUseCase(
            portfolio_repository=DjangoPortfolioRepository()
        )

        result = use_case.release_holdings(
            client_id=client_id, symbol=symbol, quantity=quantity
        )

        return JsonResponse(data=result.to_dict(), status=result.code)
