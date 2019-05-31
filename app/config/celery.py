from __future__ import absolute_import, unicode_literals
import os
from datetime import timedelta

from celery import Celery

DJANGO_SETTINGS_MODULE = os.environ.get('DJANGO_SETTINGS_MODULE')
if not DJANGO_SETTINGS_MODULE or DJANGO_SETTINGS_MODULE == 'config.settings':
    DJANGO_SETTINGS_MODULE = 'config.settings.local'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', DJANGO_SETTINGS_MODULE)

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

#
# from celery.schedules import crontab
#
# app.conf.beat_schedule = {
#     'add-every-minute-contrab': {
#         'task': 'test_beat',
#         'schedule': timedelta(seconds=30),
#         'args': (),
#     },
# }
