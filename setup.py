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
            'dexec=dockerly.wrapper:main_exec',
            'dbash=dockerly.wrapper:main_bash',
            'dpython=dockerly.wrapper:main_python',
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
