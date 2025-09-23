from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart
from .serializers import CartSerializer, CartItemSerializer
from drf_spectacular.utils import extend_schema


class CartViewSet(viewsets.ModelViewSet):
    """
    Управление элементами корзины.

    Требуется авторизация по JWT-токену. Все операции применяются только к корзине
    текущего пользователя.
    """

    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart.items.all()

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)

    @extend_schema(
        summary="Просмотреть свою корзину",
        description="Возвращает полную корзину текущего пользователя с подсчётом количества и общей суммы.",
        tags=["Корзина"],
    )
    @action(detail=False, methods=["get"], url_path="list-cart")
    def get_list_cart(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @extend_schema(
        summary="Очистить корзину",
        description="Удаляет все элементы из корзины текущего пользователя.",
        tags=["Корзина"],
    )
    @action(detail=False, methods=["delete"], url_path="clear-cart")
    def clear_cart(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()
        return Response(
            {"detail": "Корзина успешно очищена."}, status=status.HTTP_204_NO_CONTENT
        )
