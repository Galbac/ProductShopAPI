from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from shop.views import CategoryViewSet, ProductViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"products", ProductViewSet, basename="product")

urlpatterns = [
    path("", include(router.urls)),
]
