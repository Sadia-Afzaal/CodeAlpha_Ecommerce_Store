from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("complete/<str:reference>/", views.order_complete, name="order_complete"),
    path("<str:reference>/", views.order_detail, name="order_detail"),
]
