import uuid

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from catalogue.models import Category, Product


def enquiry_reference():
    return f"MAH-{timezone.now().year}-{uuid.uuid4().hex[:8].upper()}"


class QuoteRequest(models.Model):
    class Status(models.TextChoices):
        NEW = "New", "New"
        IN_REVIEW = "In Review", "In Review"
        CONTACTED = "Contacted", "Contacted"
        QUOTED = "Quoted", "Quoted"
        CLOSED = "Closed", "Closed"

    reference = models.CharField(max_length=21, unique=True, default=enquiry_reference, editable=False)
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=150)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=16)
    location = models.CharField(max_length=150)
    notes = models.TextField(blank=True, max_length=5000)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.NEW)
    internal_notes = models.TextField(blank=True, max_length=10000)
    email_status = models.CharField(max_length=12, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.reference} — {self.company}"


class QuoteItem(models.Model):
    class Unit(models.TextChoices):
        CASES = "Cases", "Cases"
        CARTONS = "Cartons", "Cartons"
        PALLETS = "Pallets", "Pallets"
        UNITS = "Units", "Units"
        OTHER = "Other", "Other"

    request = models.ForeignKey(QuoteRequest, on_delete=models.CASCADE, related_name="items")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="quote_items")
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="quote_items"
    )
    category_name = models.CharField(max_length=150)
    product_name = models.CharField(max_length=150, blank=True)
    requested_product = models.CharField(max_length=500)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    unit = models.CharField(max_length=10, choices=Unit.choices, default=Unit.CASES)

    def __str__(self):
        return f"{self.category_name}: {self.requested_product} ({self.quantity} {self.unit})"


class EnquiryRateLimit(models.Model):
    key = models.CharField(max_length=64, primary_key=True)
    hits = models.PositiveSmallIntegerField(default=0)
    window_started_at = models.DateTimeField(default=timezone.now)

