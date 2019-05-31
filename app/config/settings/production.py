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

# CELERY + Redis
CELERY_BROKER_URL = secrets['AWS_ELASTICACHE_REDIS']
CELERY_RESULT_BACKEND = secrets['AWS_ELASTICACHE_REDIS']

# # CELERY_BEAT
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TAST_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Seoul'


# 로컬에서 production 환경의 runserver, shell_plus 실행 시 로깅파일 생성 안되도록 설정
local_command = ['runserver', 'shell_plus', 'shell']
for command in local_command:
    if command in sys.argv:
        print(command)
        break

else:
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

