import json
import logging

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

logger = logging.getLogger("stock")


@method_decorator(csrf_exempt, name="dispatch")
class PortfolioView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        client_id = "7a82a0d7197b422c9f884fab0975359a"

        use_case = GetPortfolioUseCase(portfolio_repository=DjangoPortfolioRepository())

        result = use_case.get_portfolio(client_id=client_id)

        return JsonResponse(data=result.to_dict(), status=result.code)
