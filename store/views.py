from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Category, Product, Review


def home(request):
    featured = Product.objects.filter(is_active=True, is_featured=True)[:8]
    if not featured:
        featured = Product.objects.filter(is_active=True)[:8]
    new_arrivals = Product.objects.filter(is_active=True).order_by("-created_at")[:8]
    on_sale = [p for p in Product.objects.filter(is_active=True) if p.on_sale][:8]
    categories = Category.objects.all()
    context = {
        "featured": featured,
        "new_arrivals": new_arrivals,
        "on_sale": on_sale,
        "categories": categories,
    }
    return render(request, "store/home.html", context)


def product_list(request, category_slug=None):
    products = Product.objects.filter(is_active=True).select_related("category")
    category = None

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    query = request.GET.get("q", "").strip()
    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(brand__icontains=query)
            | Q(tagline__icontains=query)
        )

    sort = request.GET.get("sort", "")
    sort_map = {
        "price_asc": "price",
        "price_desc": "-price",
        "newest": "-created_at",
        "name": "name",
    }
    products = products.order_by(sort_map.get(sort, "-created_at"))

    paginator = Paginator(products, 9)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)

    # Preserve filters when building pagination links.
    params = request.GET.copy()
    params.pop("page", None)

    context = {
        "category": category,
        "categories": Category.objects.all(),
        "page_obj": page_obj,
        "products": page_obj.object_list,
        "query": query,
        "sort": sort,
        "total_count": paginator.count,
        "querystring": params.urlencode(),
    }
    return render(request, "store/product_list.html", context)


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related("category"), slug=slug, is_active=True
    )
    related = (
        Product.objects.filter(category=product.category, is_active=True)
        .exclude(pk=product.pk)[:4]
    )
    reviews = product.reviews.select_related("user")
    user_has_reviewed = (
        request.user.is_authenticated
        and reviews.filter(user=request.user).exists()
    )
    context = {
        "product": product,
        "related": related,
        "reviews": reviews,
        "user_has_reviewed": user_has_reviewed,
        "rating_range": [1, 2, 3, 4, 5],
    }
    return render(request, "store/product_detail.html", context)


@login_required
def add_review(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    if request.method == "POST":
        try:
            rating = int(request.POST.get("rating", 5))
        except (TypeError, ValueError):
            rating = 5
        rating = max(1, min(5, rating))
        comment = request.POST.get("comment", "").strip()
        Review.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={"rating": rating, "comment": comment},
        )
        messages.success(request, "Thanks! Your review has been posted.")
    return redirect(product.get_absolute_url())


def about(request):
    return render(request, "store/about.html")
