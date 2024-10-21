"""This module defines the development settings for the Django project.

Attributes:
    DEBUG (bool): Debug mode flag.
    ALLOWED_HOSTS (list): List of allowed hosts for development.
    INTERNAL_IPS (list): List of internal IPs for development.
    INSTALLED_APPS (list): List of installed apps, including debug toolbar.
    MIDDLEWARE (list): List of middleware, including debug toolbar middleware.
"""

from .base import *

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

INTERNAL_IPS = ["127.0.0.1", "::1"]

INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware", *MIDDLEWARE]
