from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from cart.cart import Cart

from .forms import CheckoutForm
from .models import Order, OrderItem


def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.info(request, "Your cart is empty — add something you love first!")
        return redirect("store:product_list")

    initial = {}
    if request.user.is_authenticated:
        profile = getattr(request.user, "profile", None)
        initial = {
            "full_name": request.user.get_full_name() or request.user.username,
            "email": request.user.email,
        }
        if profile:
            initial.update(
                {
                    "phone": profile.phone,
                    "address": profile.address,
                    "city": profile.city,
                    "postal_code": profile.postal_code,
                    "country": profile.country,
                }
            )

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                if request.user.is_authenticated:
                    order.user = request.user
                order.subtotal = cart.subtotal
                order.shipping = cart.shipping
                order.tax = cart.tax
                order.total = cart.total
                order.status = Order.Status.PAID
                order.save()

                for item in cart:
                    product = item["product"]
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        product_name=product.name,
                        price=item["price"],
                        quantity=item["quantity"],
                    )
                    # Decrement stock.
                    product.stock = max(0, product.stock - item["quantity"])
                    product.save(update_fields=["stock"])

            cart.clear()
            request.session["last_order"] = order.reference
            return redirect("orders:order_complete", reference=order.reference)
    else:
        form = CheckoutForm(initial=initial)

    return render(request, "orders/checkout.html", {"form": form, "cart": cart})


def order_complete(request, reference):
    order = get_object_or_404(Order, reference=reference)
    # Only allow viewing your own most recent order (guest via session).
    if order.user and order.user != request.user:
        if request.session.get("last_order") != reference:
            messages.error(request, "You don't have access to that order.")
            return redirect("store:home")
    return render(request, "orders/complete.html", {"order": order})


def order_detail(request, reference):
    order = get_object_or_404(Order, reference=reference)
    if order.user != request.user and not request.user.is_staff:
        if request.session.get("last_order") != reference:
            messages.error(request, "You don't have access to that order.")
            return redirect("store:home")
    return render(request, "orders/detail.html", {"order": order})
