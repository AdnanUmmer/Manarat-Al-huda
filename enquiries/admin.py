from django.contrib import admin

from .models import EnquiryRateLimit, QuoteItem, QuoteRequest


class QuoteItemInline(admin.TabularInline):
    model = QuoteItem
    extra = 0
    can_delete = False
    readonly_fields = ("category", "product", "category_name", "product_name", "requested_product", "quantity", "unit")


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ("reference", "company", "name", "email", "status", "email_status", "created_at")
    list_filter = ("status", "email_status", "created_at")
    search_fields = ("reference", "company", "name", "email", "phone")
    date_hierarchy = "created_at"
    readonly_fields = (
        "reference", "name", "company", "email", "phone", "location", "notes", "created_at", "email_status"
    )
    fields = (
        "reference", "status", "email_status", "created_at", "name", "company", "email", "phone", "location",
        "notes", "internal_notes",
    )
    inlines = (QuoteItemInline,)
    list_per_page = 50

    def has_add_permission(self, request):
        return False


@admin.register(EnquiryRateLimit)
class EnquiryRateLimitAdmin(admin.ModelAdmin):
    list_display = ("key", "hits", "window_started_at")
    readonly_fields = ("key", "hits", "window_started_at")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

