import os
import sys
import shlex
from benedict import BeneDict


def is_in_path(file, folder):
    """
    Disallow symlinks
    https://stackoverflow.com/questions/3812849/how-to-check-whether-a-directory-is-a-sub-directory-of-another-directory
    """
    folder = os.path.join(os.path.realpath(folder), '')
    file = os.path.realpath(file)  # expand symlinks to real path

    # return true, if the common prefix of both is equal to directory
    # e.g. /a/b/c/d.rst and directory is /a/b, the common prefix is /a/b
    return os.path.commonprefix([file, folder]) == folder


# docker run -ti  -v /sailhome/jimfan/vision:/home/jimfan/vision:rw $(URL) bash
class Dockerly:
    def __init__(self, config_file='~/.dockerly.yml'):
        try:
            self.config = BeneDict.load_yaml_file(os.path.expanduser(config_file))
        except FileNotFoundError:
            print('must specify a config file ~/.dockerly.yml')
            raise
        for key in ['container_root', 'host_root', 'default_image']:
            assert key in self.config, 'config "{}" missing'.format(key)
        self.container_root = self.config.container_root
        assert os.path.isabs(self.container_root)
        # must use realpath, otherwise relative path will be wrong
        self.host_root = os.path.realpath(os.path.expanduser(self.config.host_root))
        self.default_image = self.config.default_image
        self._dry_run = False

    def _run_system(self, cmd):
        if self._dry_run:
            print('>>', cmd)
        else:
            os.system(cmd)

    def get_mount_option(self, host_root, container_root, read_only=False):
        host_root = os.path.expanduser(host_root)
        if read_only:
            read_option = 'ro'
        else:
            read_option = 'rw'
        return '-v {}:{}:{}'.format(host_root, container_root, read_option)

    def dry_run(self, dry_run):
        self._dry_run = dry_run
        return self

    def run(self, cmd):
        cmd = 'docker run -ti --privileged {} {} {}'.format(
            self.get_mount_option(self.host_root, self.container_root),
            self.default_image,
            shlex.quote(cmd),
        )
        self._run_system(cmd)

    def run_from_cwd(self, cmd):
        """
        Change relative cwd ("current working dir") in the docker container        
        """
        host_cwd = os.getcwd()
        assert is_in_path(host_cwd, self.host_root), \
            'you must run this command within subpaths of `host_root` (in ~/.dockerly.yml) because it will be projected into relative path within the container.'
        host_relpath = os.path.relpath(host_cwd, self.host_root)
        container_abspath = os.path.join(self.container_root, host_relpath)
        cmd = 'docker run -ti --privileged --workdir="{}" {} {} {}'.format(
            container_abspath,
            self.get_mount_option(self.host_root, self.container_root),
            self.default_image,
            shlex.quote(cmd),
        )
        self._run_system(cmd)


def _collect_sysargs():
    args = sys.argv[1:]
    if len(args) == 1:
        return args[0]
    else:
        return ' '.join(map(shlex.quote, args))


def main_exec():
    cmd = _collect_sysargs()
    wrapper = Dockerly()
    if cmd.strip() == '':
        cmd = 'bash'  # run interative by default
    wrapper.run(cmd)


def main_bash():
    cmd = _collect_sysargs()
    wrapper = Dockerly()
    if cmd.strip() == '':
        cmd = 'bash'  # run interative by default
    wrapper.run_from_cwd(cmd)


def main_python():
    cmd = _collect_sysargs()
    wrapper = Dockerly()
    wrapper.run_from_cwd('python ' + cmd)
