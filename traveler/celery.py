import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'traveler.setings')

app = Celery('traveler')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()