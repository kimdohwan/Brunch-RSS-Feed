#!/usr/bin/env bash

IDENTITY_FILE="$HOME/.ssh/aws-ec2-doh.pem"
USER="ubuntu"
HOST="ec2-52-78-184-164.ap-northeast-2.compute.amazonaws.com"
PROJECT_DIR="$HOME/Yolo/Project"
SERVER_DIR="/home/ubuntu/Project"

# 1. ec2 에 ssh 접속
CMD_CONNECT="ssh -i ${IDENTITY_FILE} ${USER}@${HOST}"

echo " - Start deploy"

# 2. ec2 에서 실행되고 있는 런서버 종료
echo " - Kill all runserver ...."
${CMD_CONNECT} "pkill -9 -ef runserver"

# 3. 기존의 프로젝트 파일 삭제
echo " - Delete server files ...."
${CMD_CONNECT} rm -rf ${SERVER_DIR}

# 4. 새로 배포하는 프로젝트 파일 전송(복사)
echo " - Copy Project ...."
scp -q -i ${IDENTITY_FILE} -r ${PROJECT_DIR} ${USER}@${HOST}:${SERVER_DIR}



# ec2 project 로 이동, 가상환경 경로를 담음
VENV_PATH=$(${CMD_CONNECT} "cd ${SERVER_DIR} && pipenv --venv")
PYTHON_PATH="${VENV_PATH}/bin/python"
echo " - server python path = $PYTHON_PATH"

RUNSERVER_CMD="nohup ${PYTHON_PATH} manage.py runserver 0:8000"
echo " - runserver cmd = $RUNSERVER_CMD"


# 5. runserver 실행시켜주기
echo " - Execute Runserver"
export DJANGO_SETTINGS_MODULE=config.settings.dev
${CMD_CONNECT} "cd ${SERVER_DIR}/app && ${RUNSERVER_CMD}"


echo "End"





