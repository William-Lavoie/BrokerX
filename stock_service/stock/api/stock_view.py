import json
import logging

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

logger = logging.getLogger("stock")


@method_decorator(csrf_exempt, name="dispatch")
class stockView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        logger.error(request.headers)

        use_case = AddFundsTostockUseCase(
            MockPaymentServiceRepository(),
            DjangostockRepository(),
            DjangoTransactionRepository(),
        )

        uuid = "4f3251cca4f54b2e9e244189b737c8ed"
        result = use_case.get_balance(uuid)

        return JsonResponse(data=result.to_dict(), status=result.code)
