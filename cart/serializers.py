from rest_framework import serializers

from shop.models import Product
from shop.serializers import ProductSerializer
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product",
        write_only=True,
        help_text="ID продукта для добавления в корзину",
    )

    class Meta:
        model = CartItem
        fields = ["id", "product", "product_id", "quantity", "total_price"]
        read_only_fields = ["total_price"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )

    class Meta:
        model = Cart
        fields = ["id", "user", "created_at", "items", "total_items", "total_price"]
        read_only_fields = ["user", "created_at"]
