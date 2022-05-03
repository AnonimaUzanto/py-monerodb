import os
import sys

from setuptools import setup


if sys.version[:3] < '2.7' or (3, 0) < sys.version_info[:2] < (3, 7):
    sys.stderr.write('Error: py-monerodb requires at least Python 3.7\n')
    raise SystemExit(1)


def grep_version():
    path = os.path.join(os.path.dirname(__file__), "pymonerodb/__init__.py")
    with open(path) as fp:
        for line in fp:
            if line.startswith('__version__'):
                return eval(line.split()[-1])


setup(
    name="pymonerodb",
    version=grep_version(),
    description="Python Monero LMDB 'Lightning' Database reader",
    long_description="Python Monero LMDB 'Lightning' Database reader",
    long_description_content_type="text/plain",
    author="AnonimaUzanto",
    maintainer="AnonimaUzanto",
    license="MIT License",
    url="https://github.com/AnonimaUzanto/py-monerodb/",
    packages=['pymonerodb'],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Database",
        "Topic :: Database :: Database Engines/Servers",
    ],
    ext_package='pymonerodb',
    install_requires=[],
)
