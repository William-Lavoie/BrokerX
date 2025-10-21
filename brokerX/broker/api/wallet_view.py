import logging

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class GetFundsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.error("User:", request.user.email)
        funds_balance = 100
        return Response({"balance": funds_balance, "user": request.user.email})
