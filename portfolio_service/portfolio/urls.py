from django.urls import path

from portfolio.api.portfolio_view import PortfolioView

urlpatterns = [
    path("", PortfolioView.as_view(), name="portfolio"),
]