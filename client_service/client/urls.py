from django.urls import path

from .api.client_view import ClientView

urlpatterns = [
    path("", ClientView.as_view(), name="client"),
]
