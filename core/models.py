from django.core.validators import URLValidator
from django.core.validators import RegexValidator
from django.db import models


class SiteSettings(models.Model):
    company_name = models.CharField(max_length=200, default="MANARAT AL HUDA GOODS WHOLESALE TRADING L.L.C.")
    email = models.EmailField(default="Manaratalhudallc@gmail.com")
    recipient_email = models.EmailField(default="Manaratalhudallc@gmail.com")
    location = models.CharField(max_length=300, default="DIP 2, Dubai, UAE")
    phone = models.CharField(
        max_length=16,
        blank=True,
        validators=[RegexValidator(r"^\+[1-9]\d{7,14}$", "Enter a verified international phone number.")],
        help_text="Leave blank until the international number is verified.",
    )
    whatsapp = models.CharField(
        max_length=16,
        blank=True,
        validators=[RegexValidator(r"^\+[1-9]\d{7,14}$", "Enter a verified international phone number.")],
        help_text="Leave blank until the international number is verified.",
    )
    hero_headline = models.CharField(max_length=150, default="Your Partner in Everyday Wholesale Supply.")
    hero_intro = models.CharField(
        max_length=700,
        default="Based in Dubai, Manarat Al Huda supplies beverages and everyday consumer goods to trading businesses across the UAE.",
    )
    about_copy = models.CharField(
        max_length=1000,
        default="A Dubai-based trading business with a clear focus: everyday goods for the businesses that keep the UAE moving.",
    )
    cta = models.CharField(max_length=100, default="Let’s Talk Wholesale.")
    social_url = models.URLField(blank=True, validators=[URLValidator(schemes=["https"])])

    class Meta:
        verbose_name = "website contact and content"
        verbose_name_plural = "website contact and content"

    def __str__(self):
        return "Website content and contact details"

    @classmethod
    def load(cls):
        settings, _ = cls.objects.get_or_create(pk=1)
        return settings
