from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify


# Create your models here.
class Category(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        validators=[MinLengthValidator(2)],
        verbose_name="Название категории",
    )
    slug = models.SlugField(
        max_length=255, unique=True, verbose_name="Слаг категории", blank=True
    )
    image = models.ImageField(
        upload_to="categories/", verbose_name="Изображение категории"
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("name",)


class SubCategory(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        validators=[MinLengthValidator(2)],
        verbose_name="Название подкатегории",
    )
    slug = models.SlugField(
        max_length=255, unique=True, blank=True, verbose_name="Слаг подкатегории"
    )
    image = models.ImageField(
        upload_to="subcategories/", verbose_name="Изображение подкатегории"
    )
    category = models.ForeignKey(
        Category,
        related_name="subcategories",
        on_delete=models.CASCADE,
        verbose_name="Категория",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        ordering = ("name",)


class Product(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Название продукта",
        validators=[MinLengthValidator(2)],
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        verbose_name="Слаг продукта",
    )
    subcategory = models.ForeignKey(
        SubCategory,
        related_name="products",
        on_delete=models.CASCADE,
        verbose_name="Подкатегория",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1)],
        verbose_name="Цена продукта",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def category_name(self):
        return (
            self.subcategory.category.name
            if self.subcategory and self.subcategory.category
            else None
        )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name"]


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE, verbose_name="Продукт"
    )
    image_small = models.ImageField(
        upload_to="products/small/", verbose_name="Маленькое изображение"
    )
    image_medium = models.ImageField(
        upload_to="products/medium/", verbose_name="Среднее изображение"
    )
    image_large = models.ImageField(
        upload_to="products/large/", verbose_name="Большое изображение"
    )

    def __str__(self):
        return f"Изображения для {self.product.name}"

    class Meta:
        verbose_name = "Изображение продукта"
        verbose_name_plural = "Изображения продуктов"
