#!/usr/bin/env bash

pipenv lock -r > requirements.txt
echo " Create requirements.txt"

git add requirements.txt
echo " Git Add requirements.txt"

git add .secrets -f
echo " Git Add secrets"

git add --all
echo " Git Add All"

git reset HEAD lambda_function
echo " Git reset lambda_function"

eb deploy --profile doh-brunch-EB --staged
echo " Eb deploy"

git reset HEAD .secrets/ requirements.txt
echo " Git Reset secrets, requirements.txt"

rm requirements.txt
echo " Rm requirements.txt"

eb open
echo " Open eb"