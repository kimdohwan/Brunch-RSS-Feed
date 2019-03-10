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
# S3 Setting - bucket 정책 설정을 통해 S3 접속 시 사용하는 key 분리(생성 key/사용 key 다름)
AWS_ACCESS_KEY_ID = secrets['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = secrets['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = secrets['AWS_STORAGE_BUCKET_NAME']
AWS_S3_REGION_NAME = secrets['AWS_S3_REGION_NAME']
AWS_S3_SIGNATURE_VERSION = secrets['AWS_S3_SIGNATURE_VERSION']
# AWS_DEFAULT_ACL = secrets['AWS_DEFAULT_ACL']  # public read/private 옵션 설정 시 필요

# Static
STATIC_ROOT = os.path.join(ROOT_DIR, '.static')
STATIC_URL = '/static/'

# WSGI(이곳에는 적어주지 않아도 잘 동작한다.
# 아마도 request 를 받을 때는 wsgi -> settings 방향이고 respond 나 다른 경우는 반대 방향으로 추측된다
WSGI_APPLICATION = 'config.wsgi.dev.application'

# DB
DATABASES = secrets['DATABASES']
