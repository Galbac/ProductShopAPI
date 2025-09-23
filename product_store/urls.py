from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include

from django.urls import path
from django.views.generic import RedirectView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path(
        "",
        RedirectView.as_view(url="api/schema/swagger-ui/", permanent=False),
        name="index",
    ),
    path("admin/", admin.site.urls),
    path("api/", include("shop.urls")),
    path("api/", include("cart.urls")),
    path("api/token/", include("djoser.urls")),
    path("api/token/", include("djoser.urls.jwt")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
