"""This module configures Celery for the Django project, setting up the Celery
application and loading tasks from installed apps.

The configuration uses the Django settings module and the Celery library.
"""

from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
