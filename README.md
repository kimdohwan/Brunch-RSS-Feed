# Brunch RSS Feed 생성

## 프로젝트 소개

- 브런치 웹사이트(https://brunch.co.kr/)에 업데이트되는 최신글들의 RSS Feed 를 생성해주는 서비스
- 생성된 RSS Feed url 을 Feed 프로그램에 추가하여 브런치 글 구독 가능
- Feed 종류: 검색어, 작가
- 프로젝트 URL: https://idontknow.kr

## 프로젝트 영상

https://youtu.be/C9IT2Uw7oNs  
Feed 프로그램: Liferea

## 프로젝트 구성

- 사용 언어 및 프로그램 
	- AWS Elastic Beanstalk
	- Django
	- Docker
	- PostgreSQL
	- Python
	- RDS
	- Route 53
	- S3
	
- 주요내용

	브런치 웹사이트 크롤링

	- javascript 로 구현된 코드는 headless selenium 사용(검색 결과 페이지)
	- python async 비동기 http 요청(상세 페이지)
	
	RSS Feed 생성
	
	- Django Feed 커스터마이징(Project/app/articles/feed/myfeed.py)
	- MyFeed 를 상속받아 Keyword, Writer Feed 작성
	
	AWS
	
	- Elastic Beanstalk Docker 배포, Route 53(DNS), ssl 인증서
	- nginx, uwsgi 설정
	- EB extensions: 배포 후 manage.py migrate 실행
	- AWS S3: bucket 정책 설정(bucket 생성한 key 와 사용하는 Key 분리), CORS 설정
	- AWS RDS(postgresql)
	
	개발 환경 분리
	
	- local, dev, production
	- 환경 별 db 및 docker image
	
	자동화 스크립트
	
	- build.py: 숫자 입력으로 환경 별 Dockerfile 빌드
		```
		➜  Project git:(master) ./build.py
		1. base
		2. local
		3. dev
		4. production
		Choice: 1
		```
	- docker_cmd.py: 명령어, 환경 입력으로 docker 명령어 실행
		```
		➜  Project git:(master) ./docker_cmd.py --help
		usage: docker_cmd.py [-h] cmd mode

		positional arguments:
		  cmd         select cmd ['runserver', 'run']
		  mode        select docker mode ['base', 'local', 'dev', 'production']
		➜  Project git:(master) ./docker_cmd.py runserver dev 
		Performing system checks...

		System check identified no issues (0 silenced).
		March 15, 2019 - 16:22:49
		Django version 2.1.7, using settings 'config.settings.dev'
		Starting development server at http://0:8000/
		Quit the server with CONTROL-C.
		```
	- deploy.sh: eb deploy 실행 시 필요한 명령어 실행
		```
		➜  Project git:(master) ./deploy.sh 
		 Create requirements.txt
		 Git Add requirements.txt
		 Git Add secrets
		 Git Add all
		 Eb deploy
		 Git Reset secrets, requirements.txt
		 Rm requirements.txt
		 Open eb
		```

	
## Requirements

```
aiohttp==3.5.4
async-timeout==3.0.1
attrs==19.1.0
beautifulsoup4==4.7.1
boto3==1.9.111
botocore==1.12.111
certifi==2019.3.9
chardet==3.0.4
django-storages==1.7.1
django==2.1.7
docutils==0.14
idna-ssl==1.1.0 ; python_version < '3.7'
idna==2.8
jmespath==0.9.4
lxml==4.3.2
multidict==4.5.2
psycopg2-binary==2.7.7
python-dateutil==2.8.0 ; python_version >= '2.7'
pytz==2018.9
requests==2.21.0
s3transfer==0.2.0
selenium==3.141.0
six==1.12.0
soupsieve==1.8
typing-extensions==3.7.2 ; python_version < '3.7'
urllib3==1.24.1 ; python_version >= '3.4'
uwsgi==2.0.18
yarl==1.3.0

```
