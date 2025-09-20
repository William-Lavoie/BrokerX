from broker import views
from django.urls import path

urlpatterns = [
    path('', views.display_login, name="display_login"),
    path('create_user/', views.create_user, name="create_user"),
    path('confirm_passcode/', views.confirm_passcode, name="confirm_passcode"),
]