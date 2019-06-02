#!/usr/bin/env python
import argparse
import os
import subprocess
import sys

"""
- 실행: ./build.py <모드명>
- 모드에 따라서 Dockerfile 빌드
"""
MODES = ['base', 'local', 'dev', 'production']
IMANE_NAME = 'brunch-rss-feed'


def mode_fucntion(mode):
    if mode in MODES:
        cur_module = sys.modules[__name__]
        getattr(cur_module, f'build_{mode}')()
    else:
        raise ValueError


def build_base():
    try:
        subprocess.call('pipenv lock -r > requirements.txt', shell=True)
        subprocess.call(f'docker build -t {IMANE_NAME}:base -f Dockerimages/Dockerfile.base .', shell=True)
    finally:
        subprocess.call('docker rmi - f $(docker images -f "dangling=true" -q)', shell=True)


def build(mode):
    try:
        if mode in [MODES[1], MODES[2]]:
            subprocess.call('pipenv lock -r --dev > requirements.txt', shell=True)
        subprocess.call(f'docker build -t {IMANE_NAME}:{mode} -f Dockerimages/Dockerfile.{mode} .', shell=True)
    finally:
        subprocess.call('docker rmi - f $(docker images -f "dangling=true" -q)', shell=True)


def build_local():
    build(MODES[1])


def build_dev():
    build(MODES[2])


def build_production():
    build(MODES[3])


# def build_base():
#     try:
#         subprocess.call('docker build -t eb-docker:base -f Dockerfile.base .', shell=True)
#     finally:
#         os.remove('requirements.txt')
#
#
# def build_local():
#     try:
#         subprocess.call('pipenv lock -r --dev > requirements.txt', shell=True)
#         subprocess.call('docker build -t eb-docker:local -f Dockerfile.local .', shell=True)
#     finally:
#         os.remove('requirements.txt')
#
#
# def build_dev():
#     try:
#         subprocess.call('pipenv lock -r --dev > requirements.txt', shell=True)
#         subprocess.call('docker build -t eb-docker:dev -f Dockerfile.dev .', shell=True)
#     finally:
#         os.remove('requirements.txt')
#
#
# def build_production():
#     try:
#         subprocess.call('pipenv lock -r > requirements.txt', shell=True)
#         subprocess.call('docker build -t eb-docker:production -f Dockerfile.production .', shell=True)
#     finally:
#         os.remove('requirements.txt')


parser = argparse.ArgumentParser()
parser.add_argument(
    '-m', '--mode',
    help=f'select docker mode {MODES}',
    type=str
)
args = parser.parse_args()

if args.mode:
    mode = args.mode.strip().lower()
else:
    while True:
        for index, mode_name in enumerate(MODES):
            print(f'{index}. {mode_name}')
        selected_mode = input('Choice: ')
        try:
            mode_index = int(selected_mode)
            mode = MODES[mode_index]
            break
        except IndexError:
            print(f'Please Choose 1~{len(MODES)}')

if __name__ == '__main__':
    mode_fucntion(mode)
