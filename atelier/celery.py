from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atelier.settings.dev')

app = Celery('atelier')
app.conf.enable_utc = False

app.conf.update(timezone='Europe/Warsaw')

app.config_from_object(settings, namespace='CELERY')


# Celery Beat Settings
app.conf.beat_schedule = {
    'send-mail-every-tuesday': {
        'task': 'shop.tasks.send_newsletter',
        'schedule': crontab(hour=10, minute=0, day_of_week=2),
    }
}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
