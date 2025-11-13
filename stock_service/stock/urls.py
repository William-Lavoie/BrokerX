from django.urls import path
from stock.api.stock_view import StockView

urlpatterns = [
    path("", StockView.as_view(), name="wallet"),
]
