from broker import views
from django.urls import path

urlpatterns = [
    path('', views.display_login, name="display_login"),
    path('create_account/', views.create_account, name="create_account"),
]