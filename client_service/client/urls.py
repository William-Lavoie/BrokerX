from django.urls import path

from .api.client_view import ClientView

urlpatterns = [
    path("client", ClientView.as_view(), name="client"),
]
