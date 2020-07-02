from celery.schedules import crontab

from .settings import REDIS_URL

broker_url = REDIS_URL
result_backend = 'django-db'

beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'

beat_schedule = {
    'write_off_holds_from_balances': {
        'task': 'accounts.tasks.write_off_holds_from_balances',
        'schedule': crontab(minute='*/10')
    }
}
