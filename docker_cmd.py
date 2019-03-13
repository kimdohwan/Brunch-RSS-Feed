#!/usr/bin/env python
import argparse
import subprocess
import sys

MODES = ['base', 'local', 'dev', 'production']
CMDS = ['runserver', 'run']


def docker_mode(cmd, mode):
    cur_module = sys.modules[__name__]
    getattr(cur_module, f'{cmd}')(mode)


def runserver(mode):
    subprocess.call(
        f'docker run --rm -it -p 9999:8000 eb-docker:{mode} python /srv/Brunch-RSSFeed/app/manage.py runserver 0:8000',
        shell=True
    )


def run(mode):
    subprocess.call(
        f'docker run --rm -it -p 9999:8000 eb-docker:{mode} /bin/bash',
        shell=True
    )


parser = argparse.ArgumentParser()
parser.add_argument(
    'cmd',
    help=f'select cmd {CMDS}'
)
parser.add_argument(
    'mode',
    help=f'select docker mode {MODES}',
)
args = parser.parse_args()

while True:
    if args.mode in MODES and args.cmd in CMDS:
        mode = args.mode.strip().lower()
        cmd = args.cmd
        break
    else:
        print('-CMD list')
        for cmd in CMDS:
            print(cmd)
        print('\n-MODE list')
        for mode in MODES:
            print(mode)
        try:
            args.cmd, args.mode = input('\n Enter "cmd" "mode"').split()
        except ValueError:
            pass

if __name__ == '__main__':
    docker_mode(cmd, mode)
