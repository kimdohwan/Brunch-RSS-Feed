import sys

from .base import *

DEBUG = False
#
secrets = json.load(open(os.path.join(SECRET_DIR, 'production.json')))

ALLOWED_HOSTS = secrets['ALLOWED_HOSTS']

INSTALLED_APPS += [
    'storages',
]

# static file 을 aws S3 를 통해 불러오게 한다.
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'config.storages.S3StaticStorage'

WSGI_APPLICATION = 'config.wsgi.production.application'

# DB
DATABASES = secrets['DATABASES']

# runserver 테스트 할 떄는 로그파일 생성되지 않도록 설정
if 'runserver' not in sys.argv:
    # eb docker 내서 장고 에러를 기록하는 파일 생성
    LOG_FILE_PATH = '/var/log/django_error.log'
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'logfile': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': LOG_FILE_PATH,
                'maxBytes': 10485760,
                'backupCount': 10,
            }
        },
        'loggers': {
            'django': {
                'handlers': ['logfile'],
                'level': 'ERROR',
                'propagate': False,
            },
        },
    }
