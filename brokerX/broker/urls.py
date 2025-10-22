from broker import views
from django.urls import path

from .api.client_view import ClientView
from .api.otp_view import OTPView
from .api.wallet_view import WalletView

urlpatterns = [
    path("account", ClientView.as_view(), name="create_user"),
    path("passcode", OTPView.as_view(), name="confirm_passcode"),
    path("wallet", WalletView.as_view(), name="display_wallet"),
    path("add_funds_to_wallet/", views.add_funds_to_wallet, name="add_funds_to_wallet"),
    path("orders/", views.display_orders, name="display_orders"),
    path("get_name/", views.get_name, name="get_name"),
    path("get_funds/", WalletView.as_view(), name="get_funds"),
]
