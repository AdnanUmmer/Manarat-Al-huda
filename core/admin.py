from django.contrib import admin

from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Business contact", {"fields": ("company_name", "email", "recipient_email", "location", "phone", "whatsapp")}),
        ("Homepage content", {"fields": ("hero_headline", "hero_intro", "about_copy", "cta")}),
        ("Social", {"fields": ("social_url",)}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

