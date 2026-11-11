import hashlib
import logging
import smtplib
from datetime import timedelta

from django.conf import settings
from django.core.mail import EmailMessage
from django.db import IntegrityError, transaction
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from catalogue.models import Category, Product
from core.models import SiteSettings

from .forms import QuoteItemFormSet, QuoteRequestForm
from .models import EnquiryRateLimit, QuoteRequest

logger = logging.getLogger(__name__)
RATE_LIMIT = 5
RATE_WINDOW = timedelta(minutes=15)


def client_address(request):
    if settings.TRUST_PROXY:
        forwarded = request.META.get("HTTP_X_REAL_IP", "").split(",", 1)[0].strip()
        if forwarded:
            return forwarded[:100]
    return request.META.get("REMOTE_ADDR", "unknown")[:100]


def within_rate_limit(request):
    digest = hashlib.sha256(client_address(request).encode("utf-8")).hexdigest()
    now = timezone.now()
    with transaction.atomic():
        try:
            with transaction.atomic():
                bucket = EnquiryRateLimit.objects.create(key=digest, hits=1, window_started_at=now)
            return bucket.hits <= RATE_LIMIT
        except IntegrityError:
            bucket = EnquiryRateLimit.objects.select_for_update().get(key=digest)
            if bucket.window_started_at <= now - RATE_WINDOW:
                bucket.hits = 1
                bucket.window_started_at = now
            else:
                bucket.hits += 1
            bucket.save(update_fields=("hits", "window_started_at"))
            return bucket.hits <= RATE_LIMIT


def enquiry_email(quote):
    settings_record = SiteSettings.load()
    lines = [
        f"Reference: {quote.reference}",
        f"Company: {quote.company}",
        f"Name: {quote.name}",
        f"Email: {quote.email}",
        f"Phone: {quote.phone}",
        f"Location: {quote.location}",
        "",
        "Requested items:",
    ]
    for item in quote.items.select_related("category").all():
        lines.append(
            f"- {item.category_name}: {item.requested_product}; {item.quantity} {item.unit}"
        )
    if quote.notes:
        lines.extend(("", "Additional message:", quote.notes))
    EmailMessage(
        subject=f"Wholesale enquiry {quote.reference}",
        body="\n".join(lines),
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings_record.recipient_email or settings.ENQUIRY_RECIPIENT],
        reply_to=[quote.email],
    ).send(fail_silently=False)


@require_http_methods(["GET", "POST"])
def request_quote(request):
    return enquiry_page(request, contact_page=False)


@require_http_methods(["GET", "POST"])
def contact(request):
    return enquiry_page(request, contact_page=True)


def enquiry_page(request, *, contact_page):
    selected_category = None
    category_slug = request.GET.get("category", "")
    if category_slug:
        selected_category = Category.objects.filter(slug=category_slug, published=True).first()

    if request.method == "POST":
        if not within_rate_limit(request):
            return HttpResponse(
                "Too many quotation requests. Please try again in 15 minutes.",
                status=429,
                content_type="text/plain; charset=utf-8",
            )
        form = QuoteRequestForm(request.POST)
        formset = QuoteItemFormSet(request.POST, prefix="items")
        if form.is_valid() and formset.is_valid():
            if form.cleaned_data.get("website"):
                return render(request, "enquiries/confirmation.html", {"quote": None, "email_sent": False})
            with transaction.atomic():
                quote = form.save()
                formset.instance = quote
                items = formset.save(commit=False)
                for item in items:
                    item.category_name = item.category.name
                    item.product_name = item.product.name if item.product else ""
                    item.save()
                for deleted in formset.deleted_objects:
                    deleted.delete()
            try:
                enquiry_email(quote)
                email_sent = True
                quote.email_status = "Sent"
            except (OSError, smtplib.SMTPException, TimeoutError) as error:
                logger.exception("Quotation notification failed for %s", quote.reference)
                email_sent = False
                quote.email_status = "Failed"
            quote.save(update_fields=("email_status",))
            return render(
                request,
                "enquiries/confirmation.html",
                {"quote": quote, "email_sent": email_sent},
                status=201,
            )
    else:
        form = QuoteRequestForm()
        formset = QuoteItemFormSet(prefix="items")
        if selected_category:
            formset.forms[0].initial["category"] = selected_category

            selected_product = Product.objects.filter(
                category=selected_category, slug=request.GET.get("product", ""),
                published=True, archived=False,
            ).first()
            if selected_product:
                formset.forms[0].initial.update(product=selected_product, requested_product=selected_product.name)

    return render(
        request,
        "enquiries/contact.html" if contact_page else "enquiries/request_quote.html",
        {
            "form": form,
            "formset": formset,
            "has_products": Product.objects.filter(published=True, archived=False, category__published=True).exists(),
            "contact_page": contact_page,
            "selected_category": selected_category,
        },
    )

