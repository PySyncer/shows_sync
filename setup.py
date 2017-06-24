#!/usr/bin/env python
import MacOS
from setuptools import setup, find_packages


def install():
    desc = 'A Python service to sync what you watch!'
    ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__)))

    with open(os.path.join(ROOT, 'readme.md'), 'r') as r:
    long_description = r.read()

    setup(
        name='shows_sync',
        version='0.1',
        description=desc,
        long_description=long_description,
        author='PySyncer',
        author_email='',
        url='https://github.com/PySyncer/shows_sync',
        classifiers=['Operating System :: POSIX',
                     'Operating System :: Microsoft :: Windows',
                     'Operating System :: MacOS :: MacOS X',
                     'Programming Language :: Python',
                     'Programming Language :: Python :: 3.2',
                     'Programming Language :: Python :: 3.3',
                     'Programming Language :: Python :: 3.4',
                     'Programming Language :: Python :: 3.5',
                     'Programming Language :: Python :: 3.6',
                     'Programming Language :: Python :: 3 :: Only'
                     ],
        packages=find_packages(),
        install_requires=[
            'requests',
            'tmdbsimple',
            'DaemonLite',
            'tvdb-client'
        ],
    )


if __name__ == "__main__":
    install()
