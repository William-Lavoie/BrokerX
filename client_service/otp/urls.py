from django.urls import path
from otp.api.otp_view import OTPView

urlpatterns = [
    path("", OTPView.as_view(), name="passcode"),
]
