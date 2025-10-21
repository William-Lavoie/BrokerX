from broker import views
from django.urls import path

from .api.wallet_view import GetFundsView

urlpatterns = [
    path("", views.display_homepage, name="display_login"),
    path("create_user/", views.create_user, name="create_user"),
    path("confirm_passcode/", views.confirm_passcode, name="confirm_passcode"),
    path("login/", views.client_login, name="login"),
    path("client_logout/", views.client_logout, name="client_logout"),
    path("wallet/", views.display_wallet, name="display_wallet"),
    path("add_funds_to_wallet/", views.add_funds_to_wallet, name="add_funds_to_wallet"),
    path("orders/", views.display_orders, name="display_orders"),
    path("get_name/", views.get_name, name="get_name"),
   path("get_funds/", GetFundsView.as_view(), name="get-funds"),
   #   path("get_funds/", views.get_funds, name="get-funds"),

]
