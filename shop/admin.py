from django.contrib import admin

from shop.models import Category, SubCategory, Product, ProductImage


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "image"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name", "slug"]
    ordering = ["name"]


@admin.register(SubCategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "category", "image"]
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ["category"]
    search_fields = ["name", "category__name"]
    ordering = ["category", "name"]


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ["image_small", "image_medium", "image_large"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "subcategory", "price", "category"]
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ["subcategory__category", "subcategory"]
    search_fields = ["name", "subcategory__name", "subcategory__category__name"]
    inlines = [ProductImageInline]
    ordering = ["name"]

    def category(self, obj):
        return obj.category_name

    category.short_description = "Категория"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["product", "image_small", "image_medium", "image_large"]
    list_filter = ["product__subcategory__category", "product__subcategory"]
    search_fields = ["product__name"]
