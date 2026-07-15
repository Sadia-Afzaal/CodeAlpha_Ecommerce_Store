from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ("product", "product_name", "price", "quantity", "total_price")
    extra = 0

    def total_price(self, obj):
        return obj.total_price


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "reference",
        "full_name",
        "email",
        "total",
        "status",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("reference", "full_name", "email")
    readonly_fields = ("reference", "subtotal", "shipping", "tax", "total", "created_at", "updated_at")
    inlines = [OrderItemInline]
    list_editable = ("status",)
