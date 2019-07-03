
#### 소개

- 브런치 웹사이트(https://brunch.co.kr/)에 업데이트되는 최신글들의 RSS Feed 를 생성해주는 서비스

- 생성된 RSS Feed url 을 Feed 프로그램에 추가하여 브런치 글 구독 가능

- Feed 종류 : 검색어, 작가

- URL : https://www.idontknow.kr

- 프로젝트 동작 (사용한 Feed 구독 프로그램(웹): feedly)

  - 검색어 '커피' 입력 시 Feed URL 생성한 View

    ![Image](https://github.com/kimdohwan/MyStudy/blob/master/project/images/brunch/search.png)

    

  - 생성된 Feed

    ![Image](https://github.com/kimdohwan/MyStudy/blob/master/project/images/brunch/feed.png)

    

  - feedly 에서 생성된 Feed 를 구독하기

    ![Image](https://github.com/kimdohwan/MyStudy/blob/master/project/images/brunch/feedly.png)

    

  - 동작 영상 : [작가 검색](https://youtu.be/m4htPBcDcng) / [키워드 검색](https://youtu.be/1qhyNqZItJI)

- 도식화

  크롤링 속도 문제로 인해 lambda 사용하지 않도록 배포된 상태

  Django - [crawler.py](https://github.com/kimdohwan/Brunch-RSS-Feed/blob/master/app/articles/utils/crawling/crawler.py)로 크롤링 수행함

  ![Image](https://github.com/kimdohwan/Project/blob/master/blueprint_brunch.png)

[상세 기술 적용 내용](https://github.com/kimdohwan/MyStudy/blob/master/project/BrunchRssFeed.md)

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
