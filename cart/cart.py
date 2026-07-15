from decimal import Decimal

from django.conf import settings

from store.models import Product


class Cart:
    """A session-based shopping cart.

    Items are stored in the session as ``{product_id: {"quantity": int}}``.
    Prices are re-read from the DB on each request so they always reflect the
    current catalogue rather than a stale snapshot.
    """

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if cart is None:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0}
        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        # Never exceed available stock.
        if product.stock:
            self.cart[product_id]["quantity"] = min(
                self.cart[product_id]["quantity"], product.stock
            )
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        self.session.pop(settings.CART_SESSION_ID, None)
        self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            item = cart[str(product.id)].copy()
            item["product"] = product
            item["price"] = product.price
            item["total_price"] = product.price * item["quantity"]
            yield item

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        products = Product.objects.filter(id__in=self.cart.keys())
        price_map = {str(p.id): p.price for p in products}
        return sum(
            price_map.get(pid, Decimal("0")) * item["quantity"]
            for pid, item in self.cart.items()
        )

    @property
    def subtotal(self):
        return self.get_total_price()

    @property
    def shipping(self):
        # Free shipping over $75, otherwise a flat rate. Empty cart ships free.
        subtotal = self.subtotal
        if subtotal == 0 or subtotal >= Decimal("75"):
            return Decimal("0")
        return Decimal("6.99")

    @property
    def tax(self):
        # Simple 8% sales tax on the subtotal.
        return (self.subtotal * Decimal("0.08")).quantize(Decimal("0.01"))

    @property
    def total(self):
        return self.subtotal + self.shipping + self.tax
