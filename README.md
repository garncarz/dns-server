# Django DNS Server

[![Build Status](https://travis-ci.org/garncarz/dns-server.svg?branch=master)](https://travis-ci.org/garncarz/dns-server)
[![Coverage Status](https://coveralls.io/repos/garncarz/dns-server/badge.svg?branch=master&service=github)](https://coveralls.io/github/garncarz/dns-server?branch=master)
[![Docker image](https://images.microbadger.com/badges/image/garncarz/dns-server.svg)](https://microbadger.com/images/garncarz/dns-server)

This is a simple DNS service, aiming to be used as a small DynDNS server, including:

- TCP/UDP DNS protocol handler (powered by [Twisted](https://twistedmatrix.com/));
- web admin interface (powered by [Django](https://www.djangoproject.com/));
- REST API interface (enabling authorized users to set name → IP translation; powered by [Django REST framework](http://www.django-rest-framework.org/)).


## Usage

Needed: Docker, Docker Compose

You also need to have `docker-compose.yml` and `nginx-config` from this repository locally.

When installing, run:
- `docker-compose run django ./manage.py collectstatic --no-input`
- `docker-compose run django ./manage.py migrate`
- `docker-compose run django ./manage.py createsuperuser`

Start services by calling: `docker-compose up -d`

Stop services by calling: `docker-compose down`

53/TCP & 53/UDP ports are published by default.
You probably want to publish also 80/TCP, or redirect to the `django` service in your HTTP(S) proxy
(similarly to `nginx-config/dns-server.conf`).

DB is persisted in `data/db.sqlite3`.
Run `docker-compose run django ./manage.py migrate` when there's a change in the DB schema.

Also make sure your server is responsible for DNS records under the desired subdomain.
(Having a record like `dyndns.mydomain.org. 1800    IN  NS  dns.mydomain.org.`.)


### Configuration

Environment variables:
- `SECRET_KEY` – set some long random hash for Django
- `SENTRY_DSN` – optionally for logging aggregation
- `STATSD_HOST` – optionally for counting statistics


## Client usage

After creation of a (non staff) user under the web admin interface (`/auth/user/add/`), the user's credentials can be used to register/update a corresponding subdomain record, by a JSON REST API call. (The root domain is set under `/constance/config/`).

Example using [HTTPie](http://httpie.org/):

```sh
$ http -a user:password POST https://dns.mydomain.org/api/record/ ip=auto
HTTP/1.1 200 OK
Allow: GET, POST, HEAD, OPTIONS
Connection: keep-alive
Content-Type: application/json
Date: Mon, 04 Jan 2016 10:06:54 GMT
Server: nginx/1.8.0
Transfer-Encoding: chunked
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

{
    "ip": "1.2.3.4",
    "name": "user.dyndns.mydomain.org"
}
```

Checking the result:

```sh
$ dig user.dyndns.mydomain.org @dns.mydomain.org

; <<>> DiG 9.10.2-P3 <<>> user.dyndns.mydomain.org @dns.mydomain.org
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 26524
;; flags: qr ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0

;; QUESTION SECTION:
;user.dyndns.mydomain.org.         IN      A

;; ANSWER SECTION:
user.dyndns.mydomain.org.  0       IN      A       1.2.3.4

;; Query time: 35 msec
;; SERVER: 9.8.7.6#53(9.8.7.6)
;; WHEN: po I 04 11:08:24 CET 2016
;; MSG SIZE  rcvd: 55
```


## Developing

Needed extra: Python 2.7 (Twisted's DNS server isn't supported in version 3, unfortunately.)

`pip install -r requirements.txt`

`export DEBUG=1` needed.

`./manage.py makemigrations`

`./manage.py migrate` synchronizes the database schema. (Creates and uses `db.sqlite3` by default.)

Run:

- `./manage.py runserver PORT` for Django/REST interface (listens on PORT, 8000 by default)
- `./manage.py dns_server` for DNS interface (listens on TCP/UDP 10053)

`./manage.py createsuperuser` creates an admin user.

`./manage.py test` runs tests.
