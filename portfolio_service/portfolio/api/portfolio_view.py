import json
import logging

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from portfolio.adapters.django_portfolio_repository import DjangoPortfolioRepository
from portfolio.services.get_portfolio_info import GetPortfolioInfoUseCase
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

logger = logging.getLogger("portfolio")


@method_decorator(csrf_exempt, name="dispatch")
class PortfolioView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        client_id = "5a2753379b0a4db7baf166ab8946b511"

        use_case = GetPortfolioInfoUseCase(
            portfolio_repository=DjangoPortfolioRepository()
        )

        result = use_case.get_portofolio_info(client_id=client_id)

        return JsonResponse(data=result.to_dict(), status=result.code)

    def put(self, request):
        data = json.loads(request.body)

        client_id = "5a2753379b0a4db7baf166ab8946b511"
        symbol = data.get("symbol")
        name = data.get("name")
        quantity = data.get("quantity")
        buying_price = data.get("buying_price")
        current_price = data.get("current_price", None)

        use_case = GetPortfolioInfoUseCase(
            portfolio_repository=DjangoPortfolioRepository()
        )

        result = use_case.buy_holdings(
            client_id=client_id,
            symbol=symbol,
            name=name,
            quantity=quantity,
            buying_price=buying_price,
            current_price=current_price,
        )

        return JsonResponse(data=result.to_dict(), status=result.code)
