"""This module defines the base settings for the Django project.

Attributes:
    BASE_DIR (Path): The base directory of the project.
    SECRET_KEY (str): The secret key for the Django project.
    DEBUG (bool): Debug mode flag.
    ALLOWED_HOSTS (list): List of allowed hosts.
    DJANGO_APPS (list): List of default Django apps.
    LOCAL_APPS (list): List of local apps.
    THIRD_PARTY_APPS (list): List of third-party apps.
    INSTALLED_APPS (list): List of all installed apps.
    DJANGO_MIDDLEWARE (list): List of default Django middleware.
    LOCAL_MIDDLEWARE (list): List of local middleware.
    THIRD_PARTY_MIDDLEWARE (list): List of third-party middleware.
    MIDDLEWARE (list): List of all middleware.
    ROOT_URLCONF (str): Root URL configuration.
    TEMPLATES (list): List of template configurations.
    ASGI_APPLICATION (str): ASGI application path.
    WSGI_APPLICATION (str): WSGI application path.
    DATABASES (dict): Database configurations.
    AUTH_PASSWORD_VALIDATORS (list): List of password validators.
    LANGUAGE_CODE (str): Default language code.
    TIME_ZONE (str): Default time zone.
    USE_I18N (bool): Internationalization flag.
    USE_TZ (bool): Time zone usage flag.
    STATIC_URL (str): URL for static files.
    STATIC_ROOT (Path): Root directory for static files.
    STATICFILES_DIRS (list): List of directories for static files.
    DEFAULT_AUTO_FIELD (str): Default auto field type.
    CELERY_BROKER_URL (str): URL for the Celery broker.
    CELERY_RESULT_BACKEND (str): URL for the Celery result backend.
    CELERY_ACCEPT_CONTENT (list): List of accepted content types for Celery.
    CELERY_TASK_SERIALIZER (str): Serializer for Celery tasks.
    CELERY_RESULT_SERIALIZER (str): Serializer for Celery results.
    CELERY_IMPORTS (tuple): Tuple of modules to import for Celery.
    CELERY_TIMEZONE (str): Time zone for Celery.
    CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP (bool): Flag for retrying
        broker connection on startup.
    CELERY_BROKER_CHANNEL_ERROR_RETRY (bool): Flag for retrying broker
        channel errors.
    CELERY_BEAT_SCHEDULER (str): Scheduler for Celery beat.
    REST_FRAMEWORK (dict): Configuration for Django REST framework.
    SIMPLE_JWT (dict): Configuration for Simple JWT.
    DEFAULT_FROM_EMAIL (str): Default email address for sending emails.
    EMAIL_HOST (str): Email host.
    EMAIL_HOST_USER (str): Email host user.
    EMAIL_HOST_PASSWORD (str): Email host password.
    EMAIL_PORT (str): Email port.
    EMAIL_USE_TLS (bool): Flag for using TLS in email.
    TELEGRAM_BOT_TOKEN (str): Token for the Telegram bot.
    AUTH_USER_MODEL (str): Custom user model.
    API_BASE_URL (str): Base URL for the API.
    TICKER_FETCHING_API_URL (str): URL for fetching ticker data.
    TICKER_FETCHING_API_KEY (str): API key for fetching ticker data.
    TESTING (bool): Flag for testing mode.
"""

import os
import sys
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "your-default-secret-key")

DEBUG = False

ALLOWED_HOSTS = []

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

LOCAL_APPS = [
    "users.apps.UsersConfig",
    "notifications.apps.NotificationsConfig",
    "tickers.apps.TickersConfig",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "drf_yasg",
    "django_filters",
    "rest_framework_simplejwt",
    "django_celery_beat",
]

INSTALLED_APPS = [*DJANGO_APPS, *THIRD_PARTY_APPS, *LOCAL_APPS]

DJANGO_MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

LOCAL_MIDDLEWARE = []
THIRD_PARTY_MIDDLEWARE = []

MIDDLEWARE = [*DJANGO_MIDDLEWARE, *THIRD_PARTY_MIDDLEWARE, *LOCAL_MIDDLEWARE]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

ASGI_APPLICATION = "config.asgi.application"
WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DATABASE_NAME"),
        "USER": os.getenv("DATABASE_USER"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD"),
        "HOST": os.getenv("DATABASE_HOST"),
        "PORT": os.getenv("DATABASE_PORT"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"  # noqa
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"  # noqa
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = os.getenv("TIME_ZONE", "UTC")
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
CELERY_RESULT_BACKEND = os.getenv(
    "CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0"
)
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_IMPORTS = ("notifications.tasks",)
CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BROKER_CHANNEL_ERROR_RETRY = True
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "COERCE_DECIMAL_TO_STRING": False,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
}

DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_TLS = True

TELEGRAM_BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_API_TOKEN"
)

AUTH_USER_MODEL = "users.User"
API_BASE_URL = os.getenv("API_BASE_URL")
TICKER_FETCHING_API_URL = os.getenv("TICKER_FETCHING_API_URL")
TICKER_FETCHING_API_KEY = os.getenv("TICKER_FETCHING_API_KEY")

TESTING = "test" in sys.argv
