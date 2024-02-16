import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# app = Celery('proj')
app=Celery("config",
           broker="redis://localhost:6655",
           backend="redis://localhost:6655",
           
           )


app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()

