from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from shop.models import Category, Product
from shop.serializers import CategorySerializer, ProductSerializer


# Create your views here.


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Получение списка категорий продуктов с подкатегориями.

    Возвращает все категории с вложенными подкатегориями. Поддерживается пагинация (по
    10 категорий на страницу). Доступно без авторизации.
    """

    queryset = Category.objects.prefetch_related("subcategories").all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Получение списка продуктов магазина.

    Возвращает продукты с указанием категории, подкатегории, цены и изображений.
    Поддерживается пагинация (по 10 продуктов на страницу). Доступно без авторизации.
    """

    queryset = (
        Product.objects.select_related("subcategory__category")
        .prefetch_related("images")
        .all()
    )
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
