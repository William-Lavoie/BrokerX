import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
logger = logging.getLogger(__name__)
from rest_framework.exceptions import AuthenticationFailed

class GetFundsView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        print("GetFundsView GET called")
        debug_keycloak_response()
        logger.error("User:", request.user)
        logger.error("Auth:", request.auth)
        funds_balance = 100
        return Response({"balance": funds_balance, "user": request.user})


import requests

def debug_keycloak_response():
    r = requests.get("http://keycloak:7080/realms/BrokerX", verify=False)
    logger.error("Keycloak response headers:", r.headers)
    logger.error("Keycloak response content:", r.content)
    try:
        logger.error("Parsed JSON:", r.json())
    except Exception as e:
        logger.error("JSON parsing error:", e)
