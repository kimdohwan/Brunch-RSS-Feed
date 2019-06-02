# Brunch RSS Feed 생성

## 프로젝트 소개

- 브런치 웹사이트(https://brunch.co.kr/)에 업데이트되는 최신글들의 RSS Feed 를 생성해주는 서비스
- 생성된 RSS Feed url 을 Feed 프로그램에 추가하여 브런치 글 구독 가능
- Feed 종류: 검색어, 작가
- 배포 URL: https://www.idontknow.kr

## 프로젝트 영상

작가 검색: https://youtu.be/m4htPBcDcng  
키워드 검색: https://youtu.be/1qhyNqZItJI

사용한 Feed 프로그램(웹): feedly

## 프로젝트 구성

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

#### 도식화

크롤링 속도 문제로 인해 lambda 사용하지 않도록 배포된 상태(Django - [crawler.py](https://github.com/kimdohwan/Brunch-RSS-Feed/blob/master/app/articles/utils/crawling/crawler.py))

![Image](https://github.com/kimdohwan/Project/blob/master/blueprint_brunch.png)

#### 주요내용

- 브런치 웹사이트 크롤링

    - 크롤링 Tool -  Headless Chrome, Selenium
    - 비동기 처리 - Python async, aiohttp
    - <추가> Celery, Redis 를 사용해 크롤링 작업을 백그라운드에서 실행

- RSS Feed 생성

    - Django Feed 사용

- AWS
  - Django server - AWS Elastic Beanstalk
    - EC2
    - Docker application
    - EB extensions
  - ~~Crawling - AWS Lambda function~~
  - 그 외
    - Route 53(DNS), ssl 인증서
    - S3 - bucket 생성한 key 와 사용하는 Key 분리), CORS 설정
    - <추가> Elasticache - redis

- 개발 환경 분리

    - Local, Dev, Production
    - 환경 별 DB 및 Docker image

- 자동화 스크립트

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

