from .base import *

DEBUG = True
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.amazonaws.com',
]

# Static
STATIC_ROOT = os.path.join(ROOT_DIR, '.static')
STATIC_URL = '/static/'

# WSGI
WSGI_APPLICATION = 'config.wsgi.application'

# DB
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
