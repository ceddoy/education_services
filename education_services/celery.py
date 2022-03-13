import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'education_services.settings')
app = Celery("education_services")
app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks()
