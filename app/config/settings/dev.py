from .base import *

secrets = json.load(open(os.path.join(SECRET_DIR, 'dev.json')))
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.amazonaws.com',
]

# dev 에서만 사용되는 app
INSTALLED_APPS += [
    'django_extensions',
    'storages',
]

# static file 을 aws S3 를 통해 불러오게 한다.
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'config.storages.S3StaticStorage'

# Static
STATIC_ROOT = os.path.join(ROOT_DIR, '.static')
STATIC_URL = '/static/'

# WSGI(이곳에는 적어주지 않아도 잘 동작한다.
# 아마도 request 를 받을 때는 wsgi -> settings 방향이고 respond 나 다른 경우는 반대 방향으로 추측된다
WSGI_APPLICATION = 'config.wsgi.dev.application'

# DB
DATABASES = secrets['DATABASES']
