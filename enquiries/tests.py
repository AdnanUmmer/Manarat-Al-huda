from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from catalogue.models import Category
from .models import QuoteRequest


class QuoteRequestTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Soft Drinks", slug="test-soft-drinks", published=True)

    def valid_data(self):
        return {
            "name": "Test Buyer",
            "company": "QA Trading",
            "email": "buyer@example.com",
            "phone": "+971501234567",
            "location": "Dubai",
            "notes": "Test only",
            "website": "",
            "items-TOTAL_FORMS": "1",
            "items-INITIAL_FORMS": "0",
            "items-MIN_NUM_FORMS": "0",
            "items-MAX_NUM_FORMS": "20",
            "items-0-category": str(self.category.pk),
            "items-0-product": "",
            "items-0-requested_product": "Requested brand, 330 ml",
            "items-0-quantity": "10",
            "items-0-unit": "Cases",
        }

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_valid_quote_is_stored_and_notification_sent(self):
        response = self.client.post(reverse("enquiries:request-quote"), self.valid_data())
        self.assertEqual(response.status_code, 201)
        quote = QuoteRequest.objects.get()
        self.assertTrue(quote.reference.startswith("MAH-"))
        self.assertEqual(quote.items.count(), 1)
        self.assertIn(quote.reference, response.content.decode())
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(quote.email_status, "Sent")

    def test_invalid_phone_and_spam_honeypot_are_not_saved(self):
        invalid = self.valid_data()
        invalid["phone"] = "9713749234"
        self.assertEqual(self.client.post(reverse("enquiries:request-quote"), invalid).status_code, 200)
        spam = self.valid_data()
        spam["website"] = "spam"
        self.client.post(reverse("enquiries:request-quote"), spam)
        self.assertFalse(QuoteRequest.objects.exists())
