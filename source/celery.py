from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'source.settings')

app = Celery('source')

app.config_from_object('source.celery_config')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    return 'Request: {0!r}'.format(self.request.task)
