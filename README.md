# Manarat Al Huda

Django full-stack website for Manarat Al Huda Goods Wholesale Trading L.L.C. Django serves the public site, handles forms and business logic, and manages PostgreSQL data through the ORM. Django Templates render the pages; Django Admin manages content and enquiries. The former Next.js app and tooling are retained only as a migration reference and are not part of the running website.

The Django implementation keeps the existing Manrope typography, brand palette, page hierarchy, Unsplash category photography, responsive layouts and GSAP/ScrollTrigger motion. It seeds the eight existing categories without inventing products.

## Local setup

Python 3.11+ is required (verified with Python 3.13). PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python manage.py migrate
.\.venv\Scripts\python manage.py createsuperuser
.\.venv\Scripts\python manage.py runserver
```

Open `http://127.0.0.1:8000/`. Django Admin is at `http://127.0.0.1:8000/admin/`. `start-local.ps1` is an alternative launcher: it applies migrations and starts Django at the same address. Local development uses SQLite by default; configure `DATABASE_URL` or `DJANGO_DATABASE_URL` for PostgreSQL, or use `DJANGO_DATABASE_URL` to override `DATABASE_URL` locally. Do not commit `.env` or use development credentials in production.

## Public pages

- `/` — homepage and beverage carousel
- `/about/` — company information
- `/products/` — published product categories
- `/categories/<slug>/` — category landing pages and published products
- `/products/<slug>/` — published product detail
- `/trading-solutions/`, `/contact/`, `/request-quote/`, `/privacy/`
- `/robots.txt`, `/sitemap.xml`

Categories without published products show a category-specific quotation call to action rather than an empty product grid. Only published products in published categories appear publicly. Add real products through Django Admin when available; the initial database contains no product records.

## Admin and quotations

Django's built-in authentication and permissions protect `/admin/`. Admin users can manage categories, ordering, publication, category image uploads, products and product images, enquiry status/internal notes, and site contact/homepage content.

Quotation requests support up to 20 category/product lines. Server-side validation enforces international phone formatting, published category/product selection and quantities. CSRF protection, a honeypot, a database-backed limit of five requests per client IP per 15 minutes, atomic persistence and unique enquiry references are enabled. SMTP credentials are read from environment variables. A saved request remains available in Admin if email delivery fails, and the confirmation page reports that failure accurately.

The supplied phone number `9713749234` is not activated as a telephone or WhatsApp link. Phone and WhatsApp values are initially blank and should only be set in Admin after verification.

## Verification

```powershell
.\.venv\Scripts\python manage.py check
.\.venv\Scripts\python manage.py makemigrations --check --dry-run
.\.venv\Scripts\python manage.py test
.\.venv\Scripts\python manage.py runserver
# In a second terminal:
.\.venv\Scripts\python scripts\smoke.py
```

Production static files are gathered with `python manage.py collectstatic --noinput`. For local SQLite development, leave `DATABASE_URL` unset or set a `DJANGO_DATABASE_URL=sqlite:///...` override. Production must use PostgreSQL. The Django application does not require Node.js to run.

## Deployment

See [deploy/README.md](deploy/README.md) for Ubuntu, PostgreSQL, Gunicorn, Nginx, HTTPS, environment variables, backups and launch verification. See [deploy/manarat.service](deploy/manarat.service) and [deploy/nginx.conf](deploy/nginx.conf) for the supplied service/proxy templates. Replace example domain and paths before enabling.

The production hostname, PostgreSQL service, SMTP provider/credentials and verified phone number were not supplied. Email delivery and production deployment must be verified in the target environment.
