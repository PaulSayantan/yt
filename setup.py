#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from pip._internal.network.session import PipSession
from pip._internal.req import parse_requirements
from setuptools import setup

req_pkgs = parse_requirements(os.path.join(os.path.dirname(__file__), 'requirements.txt'), session=PipSession())

setup(
    name='yt',
    author='Sayantan Paul',
    description='just a simple youtube downloader to ease my life',
    author_email='paulSayantan2022@gmail.com',
    version='0.0.1',
    license='MIT',
    packages=['utils'],
    setup_requires=['setuptools>=40.0.0'],
    python_requires='>=3.7,>=3.8,>=3.9',
    install_requires=[str(r.requirement) for r in req_pkgs],
    entry_points={
        'console_scripts': [
            'yt = yt:cli',
        ],
    }
)
