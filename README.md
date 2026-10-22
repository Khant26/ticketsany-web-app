# TicketsAnywhere API

Django REST API for the TicketsAnywhere event-discovery and ticket-ordering platform. It serves the public event catalogue, authenticates customers with JWT, creates ticket orders, and provides staff-only management operations for events, banners, categories, orders, and ticket fulfilment.

## Product repository

This service is also maintained as the [`api`](https://github.com/Khant26/ticketsany/tree/api) branch of the combined [TicketsAnywhere repository](https://github.com/Khant26/ticketsany). The original repository is preserved.

## Core capabilities

- Customer registration, email verification, login, and password reset using one-time codes
- JWT access and refresh tokens
- Public event, category, and banner endpoints
- Authenticated ticket and order creation
- Customer-scoped order and ticket access
- Staff-only content management and ticket status transitions
- Cloudinary-backed media storage
- SQLite for local development and PostgreSQL through `DATABASE_URL`

## Tech stack

- Python 3.12+
- Django 5.2
- Django REST Framework
- Simple JWT
- PostgreSQL / SQLite
- Cloudinary
- Gunicorn

## Local setup

```bash
git clone https://github.com/Khant26/ticketsany-api.git
cd ticketsany-api
python -m venv .venv
```

Activate the virtual environment, then run:

```bash
python -m pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

Generate a unique `DJANGO_SECRET_KEY` before deploying. Leaving `DATABASE_URL` empty uses a local SQLite database.

## Verification

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

The test suite covers customer creation and password hashing, OTP validity and expiry, ticket/order creation, staff status rules, object permissions, and model defaults. GitHub Actions runs these checks for pushes and pull requests.

## Main API groups

The API router exposes resources under `/api/` for customers, banners, categories, events, orders, and tickets. Authentication endpoints cover registration, login, OTP verification/resending, and password recovery. See `ticketapp/urls.py` for the authoritative route list.

`GET /health` (and `/health/`) returns `{"status": "ok"}` with HTTP 200 for container and load-balancer probes.

## Environment

All configuration comes from environment variables (a local `.env` is loaded if present). See `.env.example` for the full list. The main ones:

| Variable | Purpose |
|---|---|
| `DJANGO_SECRET_KEY` | Required when `DEBUG=False` (startup fails without it). |
| `DEBUG` | `True` for local development only. |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated host names (default `localhost,127.0.0.1,.onrender.com`). |
| `DATABASE_URL` | PostgreSQL URL; empty means SQLite (`SQLITE_PATH` or `db.sqlite3`). |
| `CORS_ALLOWED_ORIGINS` | Comma-separated web-app origins, e.g. `https://ticketsany.com`. `FRONTEND_URL` / `ADMIN_URL` are still merged in. |
| `CORS_ALLOWED_ORIGIN_REGEXES` | Optional, e.g. `^https://.*\.vercel\.app$` for preview builds. |
| `CSRF_TRUSTED_ORIGINS` | Needed for Django admin login over HTTPS. |
| `EMAIL_*`, `DEFAULT_FROM_EMAIL` | SMTP settings for OTP emails. |
| `CLOUDINARY_*` | Image storage; without them uploads use local `media/`. |

Never commit `.env`, database credentials, email passwords, or Cloudinary secrets.

## Docker

```bash
docker build -t ticketsany-api .
docker run --rm -p 8000:8000 --env-file .env -e DEBUG=False -e RUN_MIGRATIONS=1 ticketsany-api
curl http://localhost:8000/health
```

The image (python:3.12-slim) collects static files at build time (served by WhiteNoise) and runs Gunicorn on `0.0.0.0:$PORT` (default `8000`) as a non-root user. `RUN_MIGRATIONS=1` applies migrations on start-up; `WEB_CONCURRENCY`, `GUNICORN_THREADS` and `GUNICORN_TIMEOUT` tune Gunicorn.

## Deployment notes

- Apply migrations before serving traffic (`RUN_MIGRATIONS=1`, or `python manage.py migrate`).
- Use `DEBUG=False` and a strong secret key in production.
- Provide origins without trailing slashes.
- Configure the web app's domain explicitly in `CORS_ALLOWED_ORIGINS`; only add the preview-domain regex if you need it.

## License

No open-source license is currently declared. All rights are reserved unless a license is added by the repository owner.
