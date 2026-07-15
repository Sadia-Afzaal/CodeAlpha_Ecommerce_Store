from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from store.models import Product

from .cart import Cart


def _cart_payload(cart):
    return {
        "count": len(cart),
        "subtotal": f"{cart.subtotal:.2f}",
        "shipping": f"{cart.shipping:.2f}",
        "tax": f"{cart.tax:.2f}",
        "total": f"{cart.total:.2f}",
    }


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_active=True)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1
    quantity = max(1, quantity)
    override = request.POST.get("override") == "true"
    cart.add(product=product, quantity=quantity, override_quantity=override)

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"ok": True, **_cart_payload(cart)})

    messages.success(request, f"Added “{product.name}” to your cart.")
    return redirect("cart:cart_detail")


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"ok": True, **_cart_payload(cart)})
    messages.info(request, f"Removed “{product.name}” from your cart.")
    return redirect("cart:cart_detail")


def cart_detail(request):
    return render(request, "cart/detail.html", {"cart": Cart(request)})
