from django.urls import path

from . import views

app_name = "catalogue"

urlpatterns = [
    path("products/", views.product_list, name="product-list"),
    path("categories/<slug:slug>/", views.category_detail, name="category-detail"),
    path("products/<slug:slug>/", views.product_detail, name="product-detail"),
]
