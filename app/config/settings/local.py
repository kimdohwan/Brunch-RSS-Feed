import sentry_sdk
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.wsgi import SentryWsgiMiddleware

from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.amazonaws.com',
]

# Static
STATIC_ROOT = os.path.join(ROOT_DIR, '.static')

# WSGI
WSGI_APPLICATION = 'config.wsgi.local.application'

# DB
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# local 에서만 사용되는 app
INSTALLED_APPS += [
    'django_extensions',
    'django_celery_beat',
    'django_celery_results',
]

# CELERY + Redis
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# CELERY_BEAT
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TAST_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Seoul'  # Celery beat가 스케줄러이기 때문에 시간에 대한 정의를 해야함

