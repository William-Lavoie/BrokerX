from django.urls import path
from wallet.api.wallet_reserve_view import WalletReserveView
from wallet.api.wallet_view import WalletView

urlpatterns = [
    path("", WalletView.as_view(), name="wallet"),
    path("reserve", WalletReserveView.as_view(), name="reserve"),
]
