[개요 및 기술 적용 내용](https://github.com/kimdohwan/MyStudy/blob/master/project/BrunchRssFeed.md)

#### 사용 언어 및 프로그램 

- AWS Elastic Beanstalk
- AWS ElastiCache
- Celery
- Django
- Docker
- Nginx
- PostgreSQL
- Python
- Redis
- RDS
- Route 53
- S3
- Sentry
- SQL

#### 개발 환경 분리

- Local, Dev, Production
- 환경 별 DB 및 Docker image

#### 자동화 스크립트

- build.py: 숫자 입력으로 환경 별 Dockerfile 빌드
  ```
  ➜  SHELL COMMAND : ./build.py
      0. base
      1. local
      2. dev
      3. production
  
  	Choice: <원하는 빌드 이미지 번호 입력>
  ```

- docker-compose.yml : ~~local~~ / dev / production 컨테이너 실행

    ```
    ➜  SHELL COMMAND : docker-compose up
    ```

- deploy.sh: eb deploy 실행 시 필요한 명령어 실행
    ```
    ➜  SHELL COMMAND : ./deploy.sh 
         Create requirements.txt
         Git Add requirements.txt
         Git Add secrets
         Git Add all
         Eb deploy
         Git Reset secrets, requirements.txt
         Rm requirements.txt
         Open eb
    ```

## Pipfile(Requirements 생성: pipenv lock -r > requirements.txt)

  ```
[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true

[dev-packages]
django-extensions = "*"
ipython = "*"
awsebcli = "*"

[packages]
django = "*"
beautifulsoup4 = "*"
lxml = "*"
requests = "*"
selenium = "*"
aiohttp = "*"
uwsgi = "*"
psycopg2-binary = "*"
boto3 = "*"
django-storages = "*"
awsebcli = "*"
celery = {extras = ["redis"],version = "*"}
django-celery-beat = "*"
django-celery-results = "*"
redis = "*"

[requires]
python_version = "3.6"
  ```