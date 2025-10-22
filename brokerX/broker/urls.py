from django.urls import path

from .api.order_view import OrderView
from .api.client_view import ClientView
from .api.otp_view import OTPView
from .api.wallet_view import WalletView

urlpatterns = [
    path("account", ClientView.as_view(), name="create_user"),
    path("passcode", OTPView.as_view(), name="confirm_passcode"),
    path("wallet", WalletView.as_view(), name="display_wallet"),
    path("order", OrderView.as_view(), name="display_orders"),
]
