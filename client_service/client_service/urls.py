"""
URL configuration for client_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import os

from client.api.client_view import MyTokenObtainPairView
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve as static_serve
from rest_framework_simplejwt.views import TokenRefreshView

from . import settings

swagger_ui_path = os.path.join(settings.BASE_DIR, "dist")
openapi_yaml_path = settings.BASE_DIR

urlpatterns = [
    path("client", include(("client.urls", "client"), namespace="client")),
    path("passcode", include(("otp.urls", "otp"), namespace="passcode")),
    path("api/token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("admin/", admin.site.urls),
    path(
        "api/",
        static_serve,
        {
            "path": "index.html",
            "document_root": swagger_ui_path,
        },
    ),
    path(
        "api/openapi.yaml",
        static_serve,
        {
            "path": "openapi.yaml",
            "document_root": openapi_yaml_path,
        },
    ),
    # Serve all other static Swagger UI files under /api/
    re_path(
        r"^api/(?P<path>.+)$",
        static_serve,
        {
            "document_root": swagger_ui_path,
        },
    ),
]
