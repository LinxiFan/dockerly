import os
import os.path as pa
import sys
import shlex
import pkg_resources
import shutil
import argparse
from .dockerly import Dockerly


DOCKERLY_YML = pa.expanduser('~/.dockerly.yml')


def _collect_sysargs():
    args = sys.argv[1:]
    if len(args) == 1:
        return args[0]
    else:
        return ' '.join(map(shlex.quote, args))


def _get_asset(name):
    "fetch from dockerly/assets"
    return pkg_resources.resource_filename('dockerly.assets', name)


def generate_config():
    print('Generating default config for Dockerly at ' + DOCKERLY_YML)
    fname = _get_asset('template_dockerly.yml')
    shutil.copyfile(fname, DOCKERLY_YML)
    print('template copied, please replace all "_fill_yours_" with your value')


def build():
    "build docker image from current working dir (must contain Dockerfile)"
    parser = argparse.ArgumentParser()
    parser.add_argument('build_dir', default=None, nargs='?',
                        help='if omitted, use `docker_build_dir` in ' + DOCKERLY_YML)
    parser.add_argument('-i', '--image', default=None,
                        help='defaults to `default_image` value in ' + DOCKERLY_YML)
    args = parser.parse_args()
    dockerly = Dockerly()
    docker_build_dir = args.build_dir or pa.expanduser(dockerly.config.docker_build_dir)
    assert pa.isdir(docker_build_dir), \
        '{} is not a build directory'.format(docker_build_dir)
    # copy assets to docker build dir unless they already exist
    for asset in ['entrypoint.py', 'requirements.txt']:
        if not pa.exists(pa.join(docker_build_dir, asset)):
            shutil.copy(_get_asset(asset), docker_build_dir)
            print('Copied docker build asset "{}" to {}'.format(asset, docker_build_dir))

    cmd = """
    docker build -t {image} --build-arg USER=$USER --build-arg UID=`id -u $USER` {build_dir}
    docker tag {image} {image}:latest
    """.format(
        image=args.image or dockerly.default_image,
        build_dir=docker_build_dir
    )
    os.system(cmd)


def run_exec():
    cmd = _collect_sysargs()
    dockerly = Dockerly()
    # dockerly.dry_run(True)
    if cmd.strip() == '':
        cmd = 'bash'  # run interative by default
    dockerly.run(cmd)


def run_bash():
    cmd = _collect_sysargs()
    dockerly = Dockerly()
    # dockerly.dry_run(True)
    if cmd.strip() == '':
        cmd = 'bash'  # run interative by default
    dockerly.run_from_cwd(cmd)


def run_python():
    cmd = _collect_sysargs()
    dockerly = Dockerly()
    dockerly.run_from_cwd('python ' + cmd)

