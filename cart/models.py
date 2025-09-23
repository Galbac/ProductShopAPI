from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

from shop.models import Product

User = get_user_model()


class Cart(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="cart", verbose_name="Пользователь"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")

    def __str__(self):
        return f"Корзина {self.user.username}"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, related_name="items", on_delete=models.CASCADE, verbose_name="Корзина"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Продукт"
    )
    quantity = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)], verbose_name="Количество"
    )

    class Meta:
        unique_together = ("cart", "product")
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"

    def __str__(self):
        return f"{self.quantity} × {self.product.name}"

    @property
    def total_price(self):
        return self.quantity * self.product.price
