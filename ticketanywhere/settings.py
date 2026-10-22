"""
Django settings for the TicketsAnywhere API.

All secrets and deployment-specific values are read from environment
variables (optionally loaded from a local, git-ignored .env file).
See .env.example for the full list.
"""

import os
from datetime import timedelta
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')


def env_bool(name, default=False):
    value = os.getenv(name)
    if value is None or value.strip() == '':
        return default
    return value.strip().lower() in ('1', 'true', 'yes', 'on')


def env_list(name, default=None):
    """Comma-separated env var -> list of non-empty, stripped values."""
    value = os.getenv(name)
    if value is None or value.strip() == '':
        return list(default or [])
    return [item.strip() for item in value.split(',') if item.strip()]


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env_bool('DEBUG', False)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    if DEBUG:
        # Local development only; never used when DEBUG is off.
        SECRET_KEY = 'django-insecure-local-development-only'
    else:
        raise ImproperlyConfigured(
            'DJANGO_SECRET_KEY must be set when DEBUG is False.'
        )

ALLOWED_HOSTS = env_list(
    'DJANGO_ALLOWED_HOSTS',
    default=['localhost', '127.0.0.1', '.onrender.com'],
)

# Origins (scheme://host[:port]) trusted for CSRF-protected POSTs such as the
# Django admin login when served over HTTPS behind a proxy.
CSRF_TRUSTED_ORIGINS = env_list('CSRF_TRUSTED_ORIGINS')

# Behind a TLS-terminating proxy (Render, Fly, Cloud Run, ...).
if env_bool('USE_X_FORWARDED_PROTO', not DEBUG):
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_COOKIE_SECURE = env_bool('SESSION_COOKIE_SECURE', not DEBUG)
CSRF_COOKIE_SECURE = env_bool('CSRF_COOKIE_SECURE', not DEBUG)

# Opt-in HTTPS hardening (enable once the API is only served over HTTPS).
SECURE_SSL_REDIRECT = env_bool('SECURE_SSL_REDIRECT', False)
SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS') or '0')
# /health must stay reachable over plain HTTP for container probes.
SECURE_REDIRECT_EXEMPT = [r'^health/?$']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ticketapp',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'cloudinary',
    'cloudinary_storage',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS
# CORS_ALLOWED_ORIGINS: comma-separated list of frontend origins, e.g.
#   https://ticketsany.com,https://www.ticketsany.com
# FRONTEND_URL / ADMIN_URL are still honoured for older deployments.
_DEFAULT_CORS_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'http://localhost:4173',
    'http://127.0.0.1:4173',
]
CORS_ALLOW_ALL_ORIGINS = env_bool('CORS_ALLOW_ALL_ORIGINS', DEBUG)
CORS_ALLOWED_ORIGINS = sorted({
    origin.rstrip('/')
    for origin in (
        env_list('CORS_ALLOWED_ORIGINS', default=_DEFAULT_CORS_ORIGINS)
        + env_list('FRONTEND_URL')
        + env_list('ADMIN_URL')
    )
    if origin
})
# Optional regexes, e.g. ^https://.*\.vercel\.app$ for Vercel preview builds.
CORS_ALLOWED_ORIGIN_REGEXES = env_list('CORS_ALLOWED_ORIGIN_REGEXES')
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'ticketanywhere.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ticketanywhere.wsgi.application'


# Database
# DATABASE_URL (e.g. postgres://user:pass@host:5432/dbname) in production;
# falls back to a local SQLite file when unset.
DATABASE_URL = os.getenv('DATABASE_URL', '').strip()
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=int(os.getenv('DB_CONN_MAX_AGE', '600')),
            conn_health_checks=True,
            ssl_require=env_bool('DB_SSL_REQUIRE', False),
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.getenv('SQLITE_PATH', str(BASE_DIR / 'db.sqlite3')),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static and media files

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Cloudinary configuration (used by the CloudinaryField image fields).
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
    'SECURE': True,
}
USE_CLOUDINARY = all(
    CLOUDINARY_STORAGE[key] for key in ('CLOUD_NAME', 'API_KEY', 'API_SECRET')
)

# Django 5.1+ ignores DEFAULT_FILE_STORAGE / STATICFILES_STORAGE; use STORAGES.
STORAGES = {
    'default': {
        'BACKEND': (
            'cloudinary_storage.storage.MediaCloudinaryStorage'
            if USE_CLOUDINARY
            else 'django.core.files.storage.FileSystemStorage'
        ),
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'ticketapp.Customer'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [],  # views control their own permissions
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

LOGIN_REDIRECT_URL = '/api/'

EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT') or '587')
EMAIL_USE_TLS = env_bool('EMAIL_USE_TLS', False)
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL') or EMAIL_HOST_USER or 'webmaster@localhost'

APPEND_SLASH = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'root': {'handlers': ['console'], 'level': os.getenv('LOG_LEVEL', 'INFO')},
}
