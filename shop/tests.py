from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from cart.models import Cart, CartItem
from shop.models import Product, Category, SubCategory

User = get_user_model()


class ProductAPITest(APITestCase):
    fixtures = [
        "fixtures/categories.json",
        "fixtures/subcategories.json",
        "fixtures/products.json",
        "fixtures/product_images.json",
    ]

    def test_get_products_list(self):
        url = reverse("product-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertGreater(len(response.data["results"]), 0)


class CartAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass123")
        self.client.force_authenticate(user=self.user)
        self.cart, _ = Cart.objects.get_or_create(user=self.user)

        self.category = Category.objects.create(
            name="Фрукты", slug="fruits", image="categories/fruits.jpg"
        )
        self.subcategory = SubCategory.objects.create(
            name="Яблоки",
            slug="apples",
            image="subcategories/apples.jpg",
            category=self.category,
        )
        self.product = Product.objects.create(
            name="Зеленое яблоко",
            slug="green-apple",
            subcategory=self.subcategory,
            price=150.00,
        )

    def test_add_product_to_cart(self):
        url = reverse("cart-item-list")
        data = {"product_id": self.product.id, "quantity": 2}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cart_item = CartItem.objects.get()
        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.quantity, 2)
        self.assertEqual(cart_item.cart.user, self.user)

        self.cart.refresh_from_db()
        self.assertEqual(self.cart.total_items, 2)
        self.assertEqual(float(self.cart.total_price), float(self.product.price) * 2)

    def test_view_cart(self):
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

        url = reverse("cart-item-list") + "list-cart/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_items"], 2)
        self.assertEqual(float(response.data["total_price"]), 300.00)
        self.assertEqual(len(response.data["items"]), 1)

    def test_update_cart_item_quantity(self):
        cart_item = CartItem.objects.create(
            cart=self.cart, product=self.product, quantity=1
        )

        url = reverse("cart-item-detail", args=[cart_item.id])
        data = {"product_id": self.product.id, "quantity": 5}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 5)

        self.cart.refresh_from_db()
        self.assertEqual(self.cart.total_items, 5)
        self.assertEqual(float(self.cart.total_price), float(self.product.price) * 5)

    def test_clear_cart(self):
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)

        url = reverse("cart-item-list") + "clear-cart/"
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CartItem.objects.count(), 0)
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.total_items, 0)
        self.assertEqual(self.cart.total_price, 0)
