from rest_framework import serializers

from shop.models import SubCategory, Category, ProductImage, Product


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ["id", "name", "slug", "image", "category"]


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "image", "subcategories"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["image_small", "image_medium", "image_large"]


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="subcategory.category.name", read_only=True)
    subcategory = serializers.CharField(source="subcategory.name", read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "slug", "category", "subcategory", "price", "images"]
