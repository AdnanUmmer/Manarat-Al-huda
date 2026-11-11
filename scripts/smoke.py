import os
import sys
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from catalogue.models import Category

base = os.environ.get("TEST_URL", "http://127.0.0.1:8000/")
public_paths = [
    "",
    "about/",
    "products/",
    "trading-solutions/",
    "contact/",
    "request-quote/",
    "privacy/",
    "admin/login/",
    "sitemap.xml",
    "robots.txt",
]
public_paths.extend(
    f"categories/{slug}/"
    for slug in Category.objects.filter(published=True).values_list("slug", flat=True)
)

for path in public_paths:
    with urlopen(urljoin(base, path)) as response:
        assert response.status == 200, path
        print("PASS", "/" + path)

with urlopen(urljoin(base, "admin/")) as response:
    assert urlparse(response.url).path == "/admin/login/", response.url
    print("PASS protected Django admin")

try:
    urlopen(urljoin(base, "products/not-real/"))
except HTTPError as error:
    assert error.code == 404, error.code
    print("PASS unknown product")
else:
    raise AssertionError("Unknown products must return HTTP 404.")
