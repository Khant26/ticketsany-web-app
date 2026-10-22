# TicketsAnywhere API - production container
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=8000

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# collectstatic only needs settings to import; use a throwaway key for this step.
RUN DJANGO_SECRET_KEY=collectstatic-build-only DEBUG=False \
    python manage.py collectstatic --noinput \
 && useradd --create-home --uid 10001 app \
 && chown -R app:app /app

USER app

EXPOSE 8000

# Runtime config comes from env vars (see .env.example). Set RUN_MIGRATIONS=1
# to apply migrations on start-up. Binds 0.0.0.0:$PORT (default 8000).
CMD ["sh", "-c", "if [ \"${RUN_MIGRATIONS:-0}\" = \"1\" ]; then python manage.py migrate --noinput; fi && exec gunicorn ticketanywhere.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers ${WEB_CONCURRENCY:-2} --threads ${GUNICORN_THREADS:-4} --timeout ${GUNICORN_TIMEOUT:-120} --access-logfile -"]
