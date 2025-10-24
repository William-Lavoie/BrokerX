from django.urls import path

from .api.client_view import ClientView
from .api.order_view import OrderView
from .api.otp_view import OTPView
from .api.wallet_view import WalletView

urlpatterns = [
    path("client", ClientView.as_view(), name="client"),
    path("passcode", OTPView.as_view(), name="passcode"),
    path("wallet", WalletView.as_view(), name="wallet"),
    path("order", OrderView.as_view(), name="order"),
]
