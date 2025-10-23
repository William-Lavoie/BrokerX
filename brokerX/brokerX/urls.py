"""
URL configuration for brokerX project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from django.views.static import serve as static_serve
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import settings

swagger_ui_path = os.path.join(settings.BASE_DIR, "static", "dist")
openapi_yaml_path = os.path.join(settings.BASE_DIR, "broker", "api")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("broker.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
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
    path('', include('django_prometheus.urls')),
]
