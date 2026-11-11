from django.db import models
from django.urls import reverse

from .presentation import image_path
from .validators import validate_category_image_url, validate_uploaded_image


class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    short_description = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to="categories/", blank=True, validators=[validate_uploaded_image])
    hero_image_url = models.URLField(max_length=1000, blank=True, validators=[validate_category_image_url])
    card_image_url = models.URLField(max_length=1000, blank=True, validators=[validate_category_image_url])
    featured = models.BooleanField(default=False)
    sort_order = models.PositiveSmallIntegerField(default=0)
    published = models.BooleanField(default=False)
    seo_title = models.CharField(max_length=150, blank=True)
    seo_description = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("sort_order", "name")
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    @property
    def hero_src(self):
        if self.image:
            return self.image.url
        return image_path(self.slug, 1440) or self.hero_image_url or self.card_image_url

    @property
    def card_src(self):
        if self.image:
            return self.image.url
        return image_path(self.slug, 480) or self.card_image_url or self.hero_image_url

    @property
    def image_srcset(self):
        if self.image or not image_path(self.slug, 480):
            return ""
        return ", ".join(f"{image_path(self.slug, width)} {width}w" for width in (480, 960, 1440))

    def get_absolute_url(self):
        return reverse("catalogue:category-detail", kwargs={"slug": self.slug})


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    brand = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    packaging = models.CharField(max_length=300, blank=True)
    case_quantity = models.CharField(max_length=100, blank=True)
    availability = models.CharField(max_length=300, blank=True)
    variants = models.CharField(max_length=2000, blank=True)
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalogue:product-detail", kwargs={"slug": self.slug})


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/", validators=[validate_uploaded_image])
    alt_text = models.CharField(max_length=200, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("sort_order", "id")

    def __str__(self):
        return self.alt_text or f"Image for {self.product}"
