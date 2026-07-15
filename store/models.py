from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Avg, Count
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    # Emoji or short icon shown in the category pill / nav.
    icon = models.CharField(max_length=8, blank=True, default="")

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("store:product_list_by_category", args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    brand = models.CharField(max_length=100, blank=True)
    tagline = models.CharField(
        max_length=200, blank=True, help_text="Short punchy one-liner for cards."
    )
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )
    compare_at_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Original price, shown struck-through to display a discount.",
    )
    image = models.ImageField(upload_to="products/", blank=True)
    image_url = models.URLField(
        blank=True,
        help_text="Optional external image URL, used when no image file is uploaded.",
    )
    stock = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug = base
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.slug])

    @property
    def display_image(self):
        """Best available image: uploaded file, then external URL, then a
        deterministic placeholder so the grid never shows a broken image."""
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return f"https://picsum.photos/seed/aurora{self.pk}/700/700"

    @property
    def in_stock(self):
        return self.stock > 0

    @property
    def on_sale(self):
        return self.compare_at_price and self.compare_at_price > self.price

    @property
    def discount_percent(self):
        if not self.on_sale:
            return 0
        return round((1 - (self.price / self.compare_at_price)) * 100)

    @property
    def rating_summary(self):
        return self.reviews.aggregate(avg=Avg("rating"), count=Count("id"))

    @property
    def average_rating(self):
        return self.rating_summary["avg"] or 0


class Review(models.Model):
    product = models.ForeignKey(
        Product, related_name="reviews", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        "auth.User", related_name="reviews", on_delete=models.CASCADE
    )
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("product", "user")

    def __str__(self):
        return f"{self.product} — {self.rating}★ by {self.user}"
