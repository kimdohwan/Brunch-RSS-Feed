# settings.base
#     공통 설정
# settings.local
#     runserver 환경
# settings.dev
#     RDS, S3 를 사용, Debug=True
# settings.production
#     실제 배포 환경, Debug=False
import os

DJANGO_SETTINGS_MODULE = os.environ.get('DJANGO_SETTINGS_MODULE')
print(DJANGO_SETTINGS_MODULE)
if not DJANGO_SETTINGS_MODULE or DJANGO_SETTINGS_MODULE == 'config.settings':
    from .local import *
