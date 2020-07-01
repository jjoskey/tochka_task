from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'source.settings')

app = Celery('source')

app.config_from_object('source.celery_config')

app.autodiscover_tasks()
