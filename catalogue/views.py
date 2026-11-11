from django.shortcuts import get_object_or_404, render

from .models import Category, Product
from .presentation import catalogue_groups


def product_list(request):
    categories = Category.objects.filter(published=True).order_by("-featured", "sort_order", "name")
    return render(request, "catalogue/product_list.html", {"categories": categories, **catalogue_groups(categories)})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug, published=True)
    products = Product.objects.filter(
        category=category, published=True, archived=False
    ).prefetch_related("images")
    related = Category.objects.filter(published=True).exclude(pk=category.pk).order_by("-featured", "sort_order")[:3]
    return render(
        request,
        "catalogue/category_detail.html",
        {"category": category, "products": products, "related_categories": related},
    )


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related("category").prefetch_related("images"),
        slug=slug,
        published=True,
        archived=False,
        category__published=True,
    )
    return render(request, "catalogue/product_detail.html", {"product": product})
