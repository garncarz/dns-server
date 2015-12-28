#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

classifiers = """\
Development Status :: 3 - Alpha
Framework :: Django
Framework :: Django :: 1.9
Intended Audience :: System Administrators
License :: OSI Approved :: GNU General Public License v2 (GPLv2)
Operating System :: POSIX :: Linux
Programming Language :: Python :: 2.7
Programming Language :: Python :: 2 :: Only
Topic :: Internet :: Name Service (DNS)
"""

setup(
    name='django-dns-server',
    version='0.1.0',
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
