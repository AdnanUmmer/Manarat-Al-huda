from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "sort_order", "featured", "published", "updated_at")
    list_editable = ("sort_order", "featured", "published")
    list_filter = ("published", "featured")
    search_fields = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("image_preview", "created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("name", "slug", "description", "short_description")}),
        ("Images", {"fields": ("image", "image_preview", "hero_image_url", "card_image_url")}),
        ("Publication", {"fields": ("sort_order", "featured", "published")}),
        ("Search appearance", {"fields": ("seo_title", "seo_description")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(description="Image preview")
    def image_preview(self, obj):
        if obj and obj.image:
            return format_html('<img src="{}" style="max-height:140px;max-width:240px" alt="">', obj.image.url)
        return "Upload an image or use the illustrative URL below."


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image", "alt_text", "sort_order")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "category", "featured", "published", "archived")
    list_filter = ("category", "published", "featured", "archived")
    search_fields = ("name", "brand", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("featured", "published", "archived")
    inlines = (ProductImageInline,)
    fieldsets = (
        (None, {"fields": ("name", "slug", "brand", "category", "description")}),
        ("Packaging and availability", {"fields": ("packaging", "case_quantity", "variants", "availability")}),
        ("Publication", {"fields": ("featured", "published", "archived")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
    readonly_fields = ("created_at", "updated_at")
