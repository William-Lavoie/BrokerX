from django.urls import path

from .views import send_test_notification, sse_notifications

urlpatterns = [
    path("", sse_notifications, name="sse_notifications"),
    path("send_test/", send_test_notification, name="send_test_notification"),
]
