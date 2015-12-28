# Django DNS Server

[![Build Status](https://travis-ci.org/garncarz/dns-server.svg?branch=master)](https://travis-ci.org/garncarz/dns-server)
[![Coverage Status](https://coveralls.io/repos/garncarz/dns-server/badge.svg?branch=master&service=github)](https://coveralls.io/github/garncarz/dns-server?branch=master)

This is a simple DNS service, aiming to be used as a small DynDNS server, including:

- TCP/UDP DNS protocol handler (listening on port 10053; powered by [Twisted](https://twistedmatrix.com/));
- web admin interface (powered by [Django](https://www.djangoproject.com/));
- REST API interface (enabling authorized users to set name → IP translation; powered by [Django REST framework](http://www.django-rest-framework.org/)).


## Installation

Needed: Python 2.7 (Twisted's DNS server isn't supported in version 3, unfortunately)

1. `git clone https://github.com/garncarz/dns-server`
2. `virtualenv2 virtualenv`
3. Make sure `virtualenv/bin` is in `PATH`.
4. `cd dns-server`
5. `pip install -r requirements.txt`


## Run

Needed: `./manage.py migrate` for synchronizing the database schema. (Creates and uses `db.sqlite3` by default.)

Run (development mode):

- `DEBUG=1 ./manage.py runserver PORT` for Django/REST interface (listens on PORT, 8000 by default)
- `DEBUG=1 ./manage.py dns_server` for DNS interface (listens on TCP/UDP 10053)

Creating an admin user: `DEBUG=1 ./manage.py createsuperuser`.


## Client usage

After creation of a (non staff) user under the web admin interface (`/auth/user/add/`), the user's credentials can be used to register/update a corresponding subdomain record, by a JSON REST API call. (The root domain is set under `/constance/config/`).

Example using [HTTPie](http://httpie.org/):

```sh
$ http -a user:password POST https://mydomain.org/api/record/ ip=auto
HTTP/1.0 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Date: Mon, 28 Dec 2015 08:10:10 GMT
Server: WSGIServer/0.1 Python/2.7.11
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

{
    "ip": "1.2.3.4",
    "name": "user.mydomain.org"
}
```

Checking the result:

```sh
$ dig user.mydomain.org @mydomain.org -p 10053

; <<>> DiG 9.10.3-P2 <<>> user.mydomain.org @mydomain.org -p 10053
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 20974
;; flags: qr ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0

;; QUESTION SECTION:
;user.mydomain.org.                IN      A

;; ANSWER SECTION:
user.mydomain.org. 0       IN      A       1.2.3.4

;; Query time: 9 msec
;; SERVER: 127.0.0.1#10053(127.0.0.1)
;; WHEN: Mon Dec 28 09:11:46 CET 2015
;; MSG SIZE  rcvd: 56
```
