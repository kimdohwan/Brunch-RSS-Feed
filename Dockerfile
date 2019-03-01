FROM        ec2-deploy:base

# uwsgi.ini 에서 사용할 변수를 Docker 에서 설정해주기
ENV         PROJECT_DIR     /srv/project

RUN         apt -y install nginx supervisor

# 셀레니엄 headless chrome 실행을 위한 패키지 설치
RUN         curl https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o /chrome.deb
RUN         dpkg -i /chrome.deb || apt-get install -yf
RUN         rm /chrome.deb

# project 폴더를 docker container 에 복사해주기
COPY        .   ${PROJECT_DIR}
WORKDIR     ${PROJECT_DIR}


# 가상환경 경로를 docker contatiner shell 에 셋팅
RUN         export VENV_PATH=$(pipenv --venv); echo $VENV_PATH;

# nginx 설정파일을 미리 준비해둔 파일로 바꿔준다
            # user root, daemon off 설정이 들어간 '기본' 설정
RUN         cp -f   ${PROJECT_DIR}/.config/nginx.conf \
                    /etc/nginx/nginx.conf && \
            # nginx 가 사용할 site 로 내 앱 설정을 넣어준다.(socket, port 설정)
            cp -f   ${PROJECT_DIR}/.config/nginx_app.conf \
                    /etc/nginx/sites-available/ && \
            # 이전에 설정해놓은 파일 삭제
            rm -f   /etc/nginx/sites-enabled/* && \
            # enabled 로 링크 생성 및 완료
            ln -sf  /etc/nginx/sites-available/nginx_app.conf \
                    /etc/nginx/sites-enabled/

# supervisor 셋팅 해준다
RUN         cp -f   ${PROJECT_DIR}/.config/supervisor_app.conf \
                    /etc/supervisor/conf.d/

# supervisord -n 명령어는 .config/supervisor_app.conf 의 명령어를 수행한다
CMD         supervisord -n