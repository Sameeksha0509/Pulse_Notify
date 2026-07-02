import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulse_notify.settings.local')

app = Celery('pulse_notify')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
