from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from store.models import Category, Product

from .models import Order


class CheckoutTests(TestCase):
    def setUp(self):
        cat = Category.objects.create(name="Audio", slug="audio")
        self.product = Product.objects.create(
            category=cat, name="Speaker", description="d", price=Decimal("50"), stock=10
        )

    def _checkout_payload(self):
        return {
            "full_name": "Jane Doe", "email": "jane@example.com", "phone": "555",
            "address": "1 St", "city": "Town", "postal_code": "0001", "country": "X",
            "notes": "",
        }

    def test_empty_cart_redirects(self):
        r = self.client.get("/orders/checkout/")
        self.assertEqual(r.status_code, 302)

    def test_full_checkout_creates_order_and_decrements_stock(self):
        self.client.post(f"/cart/add/{self.product.id}/", {"quantity": 3})
        r = self.client.post("/orders/checkout/", self._checkout_payload())
        self.assertEqual(r.status_code, 302)

        order = Order.objects.latest("created_at")
        self.assertEqual(order.item_count, 3)
        self.assertEqual(order.status, Order.Status.PAID)
        self.assertEqual(order.items.first().product_name, "Speaker")

        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 7)

    def test_order_attached_to_logged_in_user(self):
        User.objects.create_user("bob", password="pw12345678")
        self.client.login(username="bob", password="pw12345678")
        self.client.post(f"/cart/add/{self.product.id}/", {"quantity": 1})
        self.client.post("/orders/checkout/", self._checkout_payload())
        order = Order.objects.latest("created_at")
        self.assertEqual(order.user.username, "bob")

    def test_reference_is_generated(self):
        order = Order.objects.create(
            full_name="A", email="a@a.com", address="1", city="c",
            postal_code="1", country="x",
        )
        self.assertTrue(order.reference)
        self.assertEqual(len(order.reference), 8)
