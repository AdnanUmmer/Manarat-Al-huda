from urllib.parse import urlsplit

from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

MAX_IMAGE_SIZE = 8 * 1024 * 1024
MAX_IMAGE_PIXELS = 40_000_000


def validate_uploaded_image(image):
    if image.size > MAX_IMAGE_SIZE:
        raise ValidationError("Image files must be 8 MB or smaller.")
    try:
        width, height = get_image_dimensions(image)
    except (OSError, ValueError):
        raise ValidationError("Upload a valid JPEG, PNG or WebP image.") from None
    if not width or not height or width * height > MAX_IMAGE_PIXELS:
        raise ValidationError("Image dimensions must not exceed 40 megapixels.")


def validate_category_image_url(value):
    if value and urlsplit(value).hostname != "images.unsplash.com":
        raise ValidationError("Use an uploaded image or an HTTPS images.unsplash.com URL.")
