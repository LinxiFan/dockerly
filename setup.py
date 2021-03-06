import os
from setuptools import setup, find_packages


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read().strip()


setup(
    name='dockerly',
    version='0.1',
    author='Jim Fan',
    url='http://github.com/LinxiFan/dockerly',
    description='',
    license='GPLv3',
    packages=[
        package for package in find_packages() if package.startswith("dockerly")
    ],
    entry_points={
        'console_scripts': [
            'dockerly_generate_config=dockerly.main:generate_config',
            'dbuild=dockerly.main:build',
            'dexec=dockerly.main:run_exec',
            'dbash=dockerly.main:run_bash',
            'dpython=dockerly.main:run_python',
        ]
    },
    install_requires=[
        "benedict",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Programming Language :: Python :: 3"
    ],
    include_package_data=True,
    zip_safe=False
)
