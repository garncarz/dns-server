# Simple DNS server

[![Build Status](https://travis-ci.org/garncarz/dns-server.svg?branch=master)](https://travis-ci.org/garncarz/dns-server)
[![Coverage Status](https://coveralls.io/repos/garncarz/dns-server/badge.svg?branch=master&service=github)](https://coveralls.io/github/garncarz/dns-server?branch=master)

This is a simple DNS service, aiming to be used as a small DynDNS server, including:

- TCP/UDP DNS protocol handler (listening on port 10053; powered by [Twisted](https://twistedmatrix.com/));
- web admin interface (powered by [Django](https://www.djangoproject.com/));
- REST API interface (enabling authorized users to set name → IP translation; powered by [Django REST framework](http://www.django-rest-framework.org/)).


## Installation

Needed: Python 2.7 (because Twisted's DNS server isn't supported in version 3)

1. `git clone https://github.com/garncarz/dns-server`
2. `virtualenv2 virtualenv`
3. Make sure `virtualenv/bin` is in `PATH`.
4. `cd dns-server`
5. `pip install -r requirements.txt`


## Run

Needed: `./manage.py migrate` for synchronizing the database schema. (Creates and uses `db.sqlite3` by default.)

Run (development mode):

- `DEBUG=1 ./manage.py runserver PORT` for Django/REST interface (listens on PORT, 8000 by default)
- `DEBUG=1 ./dns_server.py` for DNS interface (listens on TCP/UDP 10053)
