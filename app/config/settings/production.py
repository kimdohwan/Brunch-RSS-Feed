import sys

import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration

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

# Sentry
sentry_sdk.init(
    dsn=secrets['SENTRY_DSN'],
    integrations=[
        DjangoIntegration(),
        CeleryIntegration(),
        # AioHttpIntegration(),  python version 3.7 이상 지원하는 기능, 추후 적용해 볼것
    ]
)

# 로컬에서 production 환경의 runserver, shell_plus 실행 시 로깅파일 생성 안되도록 설정
# 로컬에서 manage.py shell 을 이용한 DB 쿼리셋 작업 등을 위해 추가
local_command = ['runserver', 'shell_plus', 'shell']
for command in local_command:
    if command in sys.argv:
        print(command)
        break

else:
    # eb docker 에서 장고 에러를 기록하는 파일 생성
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


# ec2 private ip 추가 (allowd_host)
def is_ec2_linux():
    """Detect if we are running on an EC2 Linux Instance
       See http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/identify_ec2_instances.html
    """
    if os.path.isfile("/sys/hypervisor/uuid"):
        with open("/sys/hypervisor/uuid") as f:
            uuid = f.read()
            return uuid.startswith("ec2")
    return False


def get_linux_ec2_private_ip():
    """Get the private IP Address of the machine if running on an EC2 linux server"""
    from urllib.request import urlopen
    if not is_ec2_linux():
        return None
    try:
        response = urlopen('http://169.254.169.254/latest/meta-data/local-ipv4')
        ec2_ip = response.read().decode('utf-8')
        if response:
            response.close()
        return ec2_ip
    except Exception as e:
        print(e)
        return None


private_ip = get_linux_ec2_private_ip()
if private_ip:
    ALLOWED_HOSTS.append(private_ip)
