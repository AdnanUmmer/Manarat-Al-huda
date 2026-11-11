from io import BytesIO
from tempfile import TemporaryDirectory

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.test import override_settings
from PIL import Image

from .models import Category, Product


class CataloguePublicationTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Soft Drinks", slug="test-soft-drinks", published=True,
            hero_image_url="https://images.unsplash.com/photo-1622483767028-3f66f32aef97",
        )

    def test_published_category_is_browsable_without_a_product_grid(self):
        response = self.client.get(reverse("catalogue:category-detail", args=["test-soft-drinks"]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Request a quote")
        self.assertEqual(len(response.context["products"]), 0)

    def test_unpublished_category_and_product_are_not_public(self):
        self.category.published = False
        self.category.save()
        self.assertEqual(
            self.client.get(reverse("catalogue:category-detail", args=["test-soft-drinks"])).status_code,
            404,
        )

        self.category.published = True
        self.category.save()
        product = Product.objects.create(category=self.category, name="Draft", slug="draft")
        self.assertEqual(self.client.get(product.get_absolute_url()).status_code, 404)

    def test_published_product_is_public(self):
        product = Product.objects.create(
            category=self.category, name="Genuine product", slug="genuine-product", published=True
        )
        self.assertEqual(self.client.get(product.get_absolute_url()).status_code, 200)


class CategoryAdminImageTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="catalogue-admin",
            email="admin@example.com",
            password="test-password-only",
        )
        self.client.force_login(self.user)
        self.category = Category.objects.create(
            name="Upload Test",
            slug="upload-test",
            hero_image_url="https://images.unsplash.com/photo-1622483767028-3f66f32aef97",
            card_image_url="https://images.unsplash.com/photo-1622543925917-763c34d1a86e",
        )

    def test_uploaded_image_is_saved_and_overrides_category_image_urls(self):
        image_data = BytesIO()
        Image.new("RGB", (4, 4), color="blue").save(image_data, format="PNG")

        with TemporaryDirectory() as media_root, override_settings(MEDIA_ROOT=media_root):
            response = self.client.post(
                reverse("admin:catalogue_category_change", args=[self.category.pk]),
                {
                    "name": self.category.name,
                    "slug": self.category.slug,
                    "description": "",
                    "short_description": "",
                    "image": SimpleUploadedFile(
                        "upload-test.png", image_data.getvalue(), content_type="image/png"
                    ),
                    "hero_image_url": self.category.hero_image_url,
                    "card_image_url": self.category.card_image_url,
                    "sort_order": 0,
                    "published": "on",
                    "seo_title": "",
                    "seo_description": "",
                    "_save": "Save",
                },
            )

            self.assertEqual(response.status_code, 302)
            self.category.refresh_from_db()
            self.assertTrue(self.category.image)
            self.assertEqual(self.category.card_src, self.category.image.url)
            self.assertEqual(self.category.hero_src, self.category.image.url)
            self.assertTrue(self.category.image.storage.exists(self.category.image.name))
