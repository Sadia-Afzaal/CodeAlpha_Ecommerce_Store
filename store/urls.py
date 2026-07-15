from django.urls import path

from . import views

app_name = "store"

urlpatterns = [
    path("", views.home, name="home"),
    path("shop/", views.product_list, name="product_list"),
    path("shop/category/<slug:category_slug>/", views.product_list, name="product_list_by_category"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("product/<slug:slug>/review/", views.add_review, name="add_review"),
    path("about/", views.about, name="about"),
]
