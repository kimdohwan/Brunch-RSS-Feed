#!/usr/bin/env python
import argparse
import os
import subprocess
import sys

MODES = ['base', 'local', 'dev', 'production']


def mode_fucntion(mode):
    if mode in MODES:
        cur_module = sys.modules[__name__]
        print(cur_module)
        getattr(cur_module, f'build_{mode}')()
    else:
        raise ValueError


def build_base():
    try:
        subprocess.call('pipenv lock -r > requirements.txt', shell=True)
        subprocess.call('docker build -t eb-docker:base -f Dockerfile.base .', shell=True)
    finally:
        os.remove('requirements.txt')


def build_local():
    try:
        subprocess.call('pipenv lock -r --dev > requirements.txt', shell=True)
        subprocess.call('docker build -t eb-docker:local -f Dockerfile.local .', shell=True)
    finally:
        os.remove('requirements.txt')


def build_dev():
    try:
        subprocess.call('pipenv lock -r --dev > requirements.txt', shell=True)
        subprocess.call('docker build -t eb-docker:dev -f Dockerfile.dev .', shell=True)
    finally:
        os.remove('requirements.txt')


def build_production():
    try:
        subprocess.call('pipenv lock -r > requirements.txt', shell=True)
        subprocess.call('docker build -t eb-docker:production -f Dockerfile.production .', shell=True)
    finally:
        os.remove('requirements.txt')


parser = argparse.ArgumentParser()
parser.add_argument(
    '-m', '--mode',
    help=f'select docker mode {MODES}',
    type=int
)
args = parser.parse_args()

if args.mode:
    mode = args.mode.strip().lower()
else:
    while True:
        for index, mode_name in enumerate(MODES, start=1):
            print(f'{index}. {mode_name}')
        selected_mode = input('Choice: ')
        try:
            mode_index = int(selected_mode) - 1
            mode = MODES[mode_index]
            break
        except IndexError:
            print(f'Please Choose 1~{len(MODES)}')

if __name__ == '__main__':
    mode_fucntion(mode)
