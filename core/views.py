from django.conf import settings
from django.http import HttpResponse

from catalogue.presentation import catalogue_groups
from django.shortcuts import render
from django.views.decorators.cache import never_cache

from catalogue.models import Category
from catalogue.models import Product


@never_cache
def home(request):
    categories = list(Category.objects.filter(published=True).order_by("-featured", "sort_order", "name"))
    groups = catalogue_groups(categories)
    beverages = groups["beverages"]
    focus = next((category for category in beverages if category.slug == "bottled-water"), None)
    lead = next(iter(beverages or categories), None)
    return render(
        request,
        "core/home.html",
        {"categories": categories, **groups, "lead_category": lead, "focus_category": focus or lead},
    )


def about(request):
    return render(request, "core/about.html")


def trading_solutions(request):
    return render(request, "core/trading_solutions.html")


def privacy(request):
    return render(request, "core/privacy.html")


def robots(request):
    return HttpResponse(
        "User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: "
        + settings.SITE_URL + "/sitemap.xml",
        content_type="text/plain; charset=utf-8",
    )


def sitemap(request):
    from django.utils.html import escape

    urls = [
        settings.SITE_URL + "/",
        settings.SITE_URL + "/about/",
        settings.SITE_URL + "/products/",
        settings.SITE_URL + "/trading-solutions/",
        settings.SITE_URL + "/contact/",
        settings.SITE_URL + "/request-quote/",
    ]
    urls.extend(
        settings.SITE_URL + category.get_absolute_url()
        for category in Category.objects.filter(published=True)
    )
    urls.extend(
        settings.SITE_URL + product.get_absolute_url()
        for product in Product.objects.filter(published=True, archived=False, category__published=True)
    )
    entries = "".join(f"<url><loc>{escape(url)}</loc></url>" for url in urls)
    return HttpResponse(
        f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{entries}</urlset>',
        content_type="application/xml; charset=utf-8",
    )
