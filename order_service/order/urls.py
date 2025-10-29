from django.urls import path
from order.api.order_view import OrderView

urlpatterns = [
    path("", OrderView.as_view(), name="wallet"),
]
