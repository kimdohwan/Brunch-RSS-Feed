# settings.base
#     공통 설정
# settings.local
#     runserver 환경
# settings.dev
#     RDS, S3 를 사용, Debug=True
# settings.production
#     실제 배포 환경, Debug=False
from .local import *