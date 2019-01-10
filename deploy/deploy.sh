#!/usr/bin/env bash

IDENTITY_FILE="$HOME/.ssh/aws-ec2-doh.pem"
USER="ubuntu"
HOST="ec2-52-78-184-164.ap-northeast-2.compute.amazonaws.com"
PROJECT_DIR="$HOME/Yolo/Project"
SERVER_DIR="/home/ubuntu/Project"

ssh -i ${IDENTITY_FILE} ${USER}@${HOST} rm -rf ${SERVER_DIR}

scp -q -i ${IDENTITY_FILE} -r ${PROJECT_DIR} ${USER}@${HOST}:${SERVER_DIR}

