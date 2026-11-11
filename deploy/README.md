# Django production deployment

Target: Ubuntu/Debian, PostgreSQL, Gunicorn, Nginx and HTTPS. Run Gunicorn as a dedicated unprivileged `manarat` user, keep PostgreSQL private, and bind the app server to loopback.

## Initial setup

1. Install Python 3.11+, PostgreSQL, Nginx and Certbot from the operating system's supported repositories. Create a dedicated PostgreSQL database and restricted application role. Do not reuse the development database.
2. Deploy the project under `/srv/manarat/app`. Create `/srv/manarat/uploads` and `/srv/manarat/app/staticfiles`, owned by `manarat`. Create a virtual environment and install `requirements.txt`.
3. Create `/etc/manarat.env` with mode `0600`, readable only by the service account. Set `DJANGO_SECRET_KEY` to a generated secret, `DJANGO_DEBUG=false`, `DJANGO_ALLOWED_HOSTS` to the real host, and `DJANGO_CSRF_TRUSTED_ORIGINS=https://your-real-domain`. Set `DJANGO_SITE_URL`, a private PostgreSQL `DATABASE_URL`, `DJANGO_MEDIA_ROOT=/srv/manarat/uploads`, SMTP credentials, `EMAIL_FROM` and the verified notification recipient. Set `DJANGO_TRUST_PROXY=true` only when Nginx is the sole ingress and overwrites `X-Real-IP` / `X-Forwarded-Proto` as configured.
4. As the deployment user, run `python manage.py migrate`, `python manage.py createsuperuser`, and `python manage.py collectstatic --noinput`. The migrations seed the eight existing categories only. No products or default admin credentials are created. Create an admin interactively; never put its password in a committed file or command line.
5. Install `deploy/manarat.service` into `/etc/systemd/system/`. Review the venv and project paths, environment file, and writable media path. Run `systemctl daemon-reload`, enable/start the service, and inspect `journalctl -u manarat`.
6. Configure Nginx using `deploy/nginx.conf`, replace all example host/certificate/filesystem paths, and validate with `nginx -t`. Obtain and renew HTTPS certificates with Certbot. Expose only ports 80/443; keep Gunicorn and PostgreSQL private.
7. Configure sender-domain SPF/DKIM/DMARC with the chosen transactional SMTP provider. Test a real enquiry and verify both stored record and delivered message. The recipient may be the supplied Gmail account, but SMTP sender credentials must be valid.

## Environment variables

| Variable | Required production value |
|---|---|
| `DJANGO_SECRET_KEY` | Random, private secret |
| `DJANGO_DEBUG` | `false` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated real hostnames |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Comma-separated HTTPS origins |
| `DJANGO_SITE_URL` | Canonical HTTPS site URL |
| `DATABASE_URL` | Private PostgreSQL connection URL |
| `DJANGO_MEDIA_ROOT` | Persistent writable upload directory |
| `DJANGO_TRUST_PROXY` | `true` only with the trusted Nginx proxy |
| `DJANGO_SECURE_SSL_REDIRECT` | `true` |
| `DJANGO_HSTS_SECONDS` | Start with `31536000` after HTTPS is verified |
| `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD` | Provider SMTP credentials |
| `SMTP_USE_TLS`, `SMTP_USE_SSL` | Match the provider's documented transport |
| `EMAIL_FROM` | Verified sender address |
| `ENQUIRY_RECIPIENT` | Business notification recipient |

Use an `EnvironmentFile` owned by root with restrictive permissions. Never add secrets to the repository, unit file, logs, or shell history. Keep `DEBUG` disabled in production.

## Launch checks

- Confirm HTTPS redirects, allowed host validation, CSRF origin validation, HSTS, canonical URLs, sitemap and robots output.
- Confirm unauthenticated admin access redirects to Django's login and only authorised users can manage records.
- Create a draft category/product and verify it is not publicly visible. Publish the category and a genuine product, confirm they appear, then unpublish/archive and confirm they disappear. Confirm categories with no products still have a quote CTA.
- Upload valid and invalid images; verify file size/dimension limits, public image loading, persistence across restart and access permissions.
- Submit multiple quotation items, inspect their unique reference and category/product snapshots in Admin, and verify SMTP delivery. Disable SMTP in staging and confirm the enquiry still saves while the browser is told notification failed.
- Check 390 px, 768 px and 1440 px layouts, keyboard navigation, the mobile menu, carousel controls, reduced motion, and image/font/static loading.
- Confirm the contact number and WhatsApp number before enabling either in Admin.

## Backups

Schedule the supplied `backup.sh` with a dedicated PostgreSQL backup role and read access to `DJANGO_MEDIA_ROOT`. Configure `PGPASSFILE` with restrictive permissions, plus `PGDATABASE`, `PGHOST`, `PGUSER` and `BACKUP_DIR`; never put a database password in command arguments. Encrypt backups off-host and monitor backup failures.

Restore a database and media backup to an isolated staging environment regularly. Back up before schema migrations and keep the previous code release until post-deployment checks pass. No production service or database is modified by this repository setup.
