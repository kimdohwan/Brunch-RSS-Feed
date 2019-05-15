#!/usr/bin/env bash

pipenv lock -r > requirements.txt
echo " Create requirements.txt"

git add .secrets -f
echo " Git Add secrets"

git add --all
echo " Git Add All"

git reset HEAD lambda_function
echo " Git reset lambda_function"

eb deploy --profile EB_Full --staged
echo " Eb deploy"

git reset HEAD .secrets/
echo " Git Reset secrets"

eb open
echo " Open eb"