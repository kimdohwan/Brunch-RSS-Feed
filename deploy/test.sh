#!/usr/bin/env bash

IDENTITY_FILE="$HOME/.ssh/aws-ec2-doh.pem"
USER="ubuntu"
HOST="ec2-52-78-184-164.ap-northeast-2.compute.amazonaws.com"
PROJECT_DIR="$HOME/Yolo/Project"
SERVER_DIR="/home/ubuntu/Project"

# ssh 연결
CMD_CONNECT="ssh -i ${IDENTITY_FILE} ${USER}@${HOST}"

echo " - Start deploy"

echo " - Kill all runserver ...."
${CMD_CONNECT} "pkill -9 -ef runserver"

echo " - Delete server files ...."
${CMD_CONNECT} rm -rf ${SERVER_DIR}

echo " - Copy Project ...."
scp -q -i ${IDENTITY_FILE} -r ${PROJECT_DIR} ${USER}@${HOST}:${SERVER_DIR}



# ssh 연결 후, server project 로 이동, 가상환경 경로를 담음
VENV_PATH=$(${CMD_CONNECT} "cd ${SERVER_DIR} && pipenv --venv")
PYTHON_PATH="${VENV_PATH}/bin/python"
echo " - server python path = $PYTHON_PATH"

RUNSERVER_CMD="nohup ${PYTHON_PATH} manage.py runserver 0:8000"
echo " - runserver cmd = $RUNSERVER_CMD"

echo " - Execute Runserver"
${CMD_CONNECT} "cd ${SERVER_DIR}/app && ${RUNSERVER_CMD}"


echo "End"





