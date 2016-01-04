# Django DNS Server

[![Build Status](https://travis-ci.org/garncarz/dns-server.svg?branch=master)](https://travis-ci.org/garncarz/dns-server)
[![Coverage Status](https://coveralls.io/repos/garncarz/dns-server/badge.svg?branch=master&service=github)](https://coveralls.io/github/garncarz/dns-server?branch=master)

This is a simple DNS service, aiming to be used as a small DynDNS server, including:

- TCP/UDP DNS protocol handler (listening on port 10053; powered by [Twisted](https://twistedmatrix.com/));
- web admin interface (powered by [Django](https://www.djangoproject.com/));
- REST API interface (enabling authorized users to set name → IP translation; powered by [Django REST framework](http://www.django-rest-framework.org/)).


## Installation

Needed: Python 2.7 (Twisted's DNS server isn't supported in version 3, unfortunately.)

1. `git clone https://github.com/garncarz/dns-server`
2. `virtualenv2 virtualenv`
3. Make sure `virtualenv/bin` is in `PATH`.
4. `cd dns-server`
5. `pip install -r requirements.txt`


## Production use

A dedicated UNIX user (e.g. `dns`) is recommended for deployment of the application.

1. Make sure your server is reponsible for DNS records under the desired subdomain.

    Having a record like `dyndns.mydomain.org. 1800    IN  NS  dns.mydomain.org.`.

2. Route server's port 53 to 10053. (Optional, but recommended, don't run this application as root, please.)

    ```sh
    iptables -t nat -A PREROUTING -p tcp --dport 53 -j REDIRECT --to-port 10053
    iptables -t nat -A PREROUTING -p udp --dport 53 -j REDIRECT --to-port 10053
    ```

3. Configure Nginx (or other web server) for the web interface.

    ```nginx
    server {
        server_name .dns.mydomain.org;
        location / {
            include uwsgi_params;
            uwsgi_pass 127.0.0.1:10090;
        }
        location /static/ {
            alias /home/dns/static/;
        }
    }
    ```

4. Create a custom configuration file (`main/settings_local.py`), or set needed variables as system ones.

    `export SECRET_KEY=jrg2j3hrg2uy3rgy32r` (example)

5. Prepare database & static files (needed after every update).

    ```sh
    ./manage.py migrate
    ./manage.py collectstatic
    ```

6. Create an admin user.

    `./manage.py createsuperuser`

7. Run the application (both web and DNS interface).

    ```sh
    mkdir -p ~/log  # needed once
    supervisord
    ```

    Daemons can be controlled by `supervisorctl` then. Logs are stored under `~/log`.


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

`export DEBUG=1` needed.

`./manage.py migrate` synchronizes the database schema. (Creates and uses `db.sqlite3` by default.)

Run:

- `./manage.py runserver PORT` for Django/REST interface (listens on PORT, 8000 by default)
- `./manage.py dns_server` for DNS interface (listens on TCP/UDP 10053)

`./manage.py createsuperuser` creates an admin user.

`./manage.py test` runs tests.
