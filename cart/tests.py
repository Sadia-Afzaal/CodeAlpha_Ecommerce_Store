from decimal import Decimal

from django.test import TestCase

from store.models import Category, Product


class CartTests(TestCase):
    def setUp(self):
        cat = Category.objects.create(name="Audio", slug="audio")
        self.p1 = Product.objects.create(
            category=cat, name="Speaker", description="d", price=Decimal("50"), stock=10
        )
        self.p2 = Product.objects.create(
            category=cat, name="Buds", description="d", price=Decimal("30"), stock=3
        )

    def test_add_updates_count_and_totals(self):
        r = self.client.post(
            f"/cart/add/{self.p1.id}/", {"quantity": 2},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        data = r.json()
        self.assertTrue(data["ok"])
        self.assertEqual(data["count"], 2)
        self.assertEqual(data["subtotal"], "100.00")

    def test_add_respects_stock_cap(self):
        self.client.post(f"/cart/add/{self.p2.id}/", {"quantity": 99})
        r = self.client.get("/cart/")
        # p2 only has 3 in stock
        self.assertEqual(len(r.wsgi_request.session["cart"]), 1)
        self.assertEqual(r.wsgi_request.session["cart"][str(self.p2.id)]["quantity"], 3)

    def test_shipping_is_free_over_threshold(self):
        self.client.post(f"/cart/add/{self.p1.id}/", {"quantity": 2})  # $100 > $75
        r = self.client.get("/cart/")
        self.assertEqual(r.context["cart"].shipping, Decimal("0"))

    def test_shipping_charged_under_threshold(self):
        self.client.post(f"/cart/add/{self.p2.id}/", {"quantity": 1})  # $30 < $75
        r = self.client.get("/cart/")
        self.assertEqual(r.context["cart"].shipping, Decimal("6.99"))

    def test_remove(self):
        self.client.post(f"/cart/add/{self.p1.id}/", {"quantity": 1})
        self.client.post(f"/cart/remove/{self.p1.id}/")
        r = self.client.get("/cart/")
        self.assertEqual(len(r.context["cart"]), 0)
