#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

classifiers = """\
Development Status :: 3 - Alpha
Framework :: Django
Framework :: Django :: 5.2
Intended Audience :: System Administrators
License :: OSI Approved :: GNU General Public License v2 (GPLv2)
Operating System :: POSIX :: Linux
Programming Language :: Python :: 3
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Programming Language :: Python :: 3.10
Programming Language :: Python :: 3.11
Programming Language :: Python :: 3.12
Topic :: Internet :: Name Service (DNS)
"""

setup(
    name='django-dns-server',
    version='1.0.0',
    author='Ondřej Garncarz',
    author_email='ondrej@garncarz.cz',
    url='https://github.com/garncarz/dns-server',
    license='GPLv2',

    description='Simple Django/REST/Twisted DNS server',
    keywords='dns dyndns server',
    classifiers=classifiers.splitlines(),

    packages=find_packages(),
    install_requires=[
        req.split('=')[0] for req in open('requirements.txt').readlines()
    ],
)
