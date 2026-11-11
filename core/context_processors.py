from django.conf import settings

from .models import SiteSettings


def site_context(request):
    return {"site_settings": SiteSettings.load(), "canonical_url": settings.SITE_URL + request.path}
