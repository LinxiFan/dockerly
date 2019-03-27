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
            print('must specify a config file ' + config_file)
            raise
        for key in ['container_root', 'host_root', 'default_image']:
            assert key in self.config, 'config "{}" missing'.format(key)
        for k, v in self.config.items():
            if v == '_fill_yours_':
                raise ValueError('please fill in key "{}" in {}'.format(k, config_file))
        self.container_root = self.config.container_root
        assert os.path.isabs(self.container_root), \
            'container_root must be an absolute path: ' + self.container_root
        # must use realpath, otherwise relative path will be wrong
        self.host_root = os.path.realpath(os.path.expanduser(self.config.host_root))
        self.ports = self.config.ports
        self.default_image = self.config.default_image
        self._docker_exe = 'nvidia-docker' if self.config.nvidia else 'docker'
        self._dry_run = False

    def _run_system(self, cmd):
        if self._dry_run:
            print('>>', cmd)
        else:
            os.system(cmd)

    def _mount_flag(self, host_root, container_root, read_only=False):
        host_root = os.path.expanduser(host_root)
        if read_only:
            read_option = 'ro'
        else:
            read_option = 'rw'
        return '-v {}:{}:{}'.format(host_root, container_root, read_option)

    def _ports_flag(self):
        flag = ''
        for port_spec in self.ports:
            flag += '-p {} '.format(port_spec)
        return flag

    def dry_run(self, dry_run):
        self._dry_run = dry_run
        return self

    def run(self, cmd, *other_options):
        """
        other_options: flags to pass to docker run
        """
        cmd = '{docker} run -ti --privileged {others} {mount} {ports} {image} {cmd}'.format(
            docker=self._docker_exe,  # nvidia-docker
            others=' '.join(other_options),
            ports=self._ports_flag(),
            mount=self._mount_flag(self.host_root, self.container_root),
            image=self.default_image,
            cmd=shlex.quote(cmd),
        )
        # replace excessive whitespace for better dry-run:
        cmd = ' '.join(cmd.split())
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
        self.run(cmd, '--workdir="{}"'.format(container_abspath))
