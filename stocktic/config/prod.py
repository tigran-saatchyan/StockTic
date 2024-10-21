"""This module defines the production settings for the Django project.

Attributes:
    DEBUG (bool): Debug mode flag.
    ALLOWED_HOSTS (list): List of allowed hosts for production.
    SECURE_SSL_REDIRECT (bool): Flag to redirect all HTTP requests to HTTPS.
    CSRF_COOKIE_SECURE (bool): Flag to use a secure cookie for the CSRF cookie.
    SESSION_COOKIE_SECURE (bool): Flag to use a secure cookie for the
        session cookie.
    ADMINS (list): List of admin users.
"""

from .base import *

DEBUG = False

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

ADMINS = [("Admin", os.getenv("ADMIN_EMAIL"))]
