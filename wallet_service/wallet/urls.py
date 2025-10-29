from django.urls import path
from wallet.api.wallet_view import WalletView

urlpatterns = [
    path("", WalletView.as_view(), name="wallet"),
]
