from django.urls import path
from portfolio.api.portfolio_reserve_view import PortfolioReserveView
from portfolio.api.portfolio_view import PortfolioView

urlpatterns = [
    path("", PortfolioView.as_view(), name="portfolio"),
    path("reserve/", PortfolioReserveView.as_view(), name="portfolio_reserve"),
]
