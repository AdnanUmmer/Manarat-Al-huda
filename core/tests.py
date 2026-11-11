from django.test import TestCase

from .models import SiteSettings


class SiteSettingsTests(TestCase):
    def test_default_contact_details_do_not_activate_unverified_phone(self):
        settings = SiteSettings.load()
        self.assertEqual(settings.email, "Manaratalhudallc@gmail.com")
        self.assertEqual(settings.location, "DIP 2, Dubai, UAE")
        self.assertEqual(settings.phone, "")
        self.assertEqual(settings.whatsapp, "")
