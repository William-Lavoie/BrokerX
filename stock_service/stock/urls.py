from django.urls import path
from stock.api.stock_view import StockView
from stock.api.top_of_book_view import TopOfBookView

urlpatterns = [
    path("", StockView.as_view(), name="wallet"),
    path("top-of-book", TopOfBookView.as_view(), name="top-of-book")
]
