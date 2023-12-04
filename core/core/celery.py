from __future__ import absolute_import, unicode_literals
import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
celery = Celery(
    "core",
    include=['user.tasks'],
)
celery.config_from_object("django.conf:settings", namespace="CELERY")
celery.autodiscover_tasks()
