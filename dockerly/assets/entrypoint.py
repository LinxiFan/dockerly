#!/usr/bin/env python
"""
This file is meant to be ENTRYPOINT in Dockerfile
"""
import os
import sys
import shlex
import shutil


def init():
    pass
    # os.system('Xdummy > /dev/null 2>&1 &')
    # if os.path.exists('/etc/secrets/mjkey.txt'):
    #     shutil.copy('/etc/secrets/mjkey.txt', '/root/.mujoco/mjkey.txt')
    # os.system('python -c "import mujoco_py"')
    # os.environ['DISPLAY'] = ':0'


def run_cmd_list(args):
    if len(args) == 1:
        os.system(args[0])
    else:  # docker run
        os.system(' '.join(map(shlex.quote, args)))


init()
run_cmd_list(sys.argv[1:])
