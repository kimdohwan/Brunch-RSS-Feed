FROM            dosio0102/eb-docker-brunch:base
MAINTAINER      dosio0102@gmail.com

RUN             apt -y update && apt -y dist-upgrade
# uwsgi 설치에 필요한 build_essentiol, chrome driver 설치에 필요한 curl
RUN             apt -y install build-essential curl
RUN             apt -y install nginx supervisor

# pipenv lock -r 로 생성된 requirements.txt 로 필요 패키지 install
COPY            ./requirements.txt  /srv/
RUN             pip install -r /srv/requirements.txt

# 셀레니엄 headless chrome 실행을 위한 패키지 설치
RUN             curl https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o /chrome.deb
RUN             dpkg -i /chrome.deb || apt-get install -yf
RUN             rm /chrome.deb

ENV             BUILD_MODE  production
ENV             DJANGO_SETTINGS_MODULE  config.settings.${BUILD_MODE}

COPY            .       /srv/Brunch-RSSFeed

# nginx 설정파일을 미리 준비해둔 파일로 바꿔준다
            # user root, daemon off 설정이 들어간 '기본' 설정
RUN         cp -f   /srv/Brunch-RSSFeed/.config/${BUILD_MODE}/nginx.conf \
                    /etc/nginx/nginx.conf && \
            # nginx 가 사용할 site 로 내 앱 설정을 넣어준다.(socket, port 설정)
            cp -f   /srv/Brunch-RSSFeed/.config/${BUILD_MODE}/nginx_app.conf \
                    /etc/nginx/sites-available/ && \
            # 이전에 설정해놓은 파일 삭제
#            rm -f   /etc/nginx/sites-enabled/* && \
            # enabled 로 링크 생성 및 완료
            ln -sf  /etc/nginx/sites-available/nginx_app.conf \
                    /etc/nginx/sites-enabled/

# supervisor 셋팅 해준다
RUN         cp -f   /srv/Brunch-RSSFeed/.config/${BUILD_MODE}/supervisor_app.conf \
                    /etc/supervisor/conf.d/

# Docker container 에서 eb 의 reverse proxy 로 요청을 받는 port(eb 설정에 필요)
# 만약 7000번 port 로 요청을 받는다고 Dockerfile 에 작성했는데 연결이 안될 경우에는
# 현재 docker container 의 nginx가 몇번 port 로 요청을 받게 설정되어있는지 확인해야 한다.
# nginx 설정 파일에서 확인가능.
EXPOSE      7000

# supervisord -n 명령어는 .config/supervisor_app.conf 의 명령어를 수행한다
CMD         supervisord -n
