#!/usr/bin/env python2

import os
import django
from twisted.internet import reactor, defer
from twisted.names import client, dns, error, server

from main import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

from dns.models import Record


class MyResolver(object):
    def query(self, query, timeout=None):
        try:
            name = query.name.name
            rec = Record.objects.get(name=name)
            answer = dns.RRHeader(
                name=name,
                payload=dns.Record_A(address=rec.ip),
            )
            answers = [answer]
            authority = []
            additional = []
            return defer.succeed((answers, authority, additional))
        except Record.DoesNotExist:
            return defer.fail(error.DomainError())


def main():
    factory = server.DNSServerFactory(
        clients=[MyResolver(),
                 client.Resolver(resolv='/etc/resolv.conf')]
    )
    protocol = dns.DNSDatagramProtocol(controller=factory)

    reactor.listenUDP(settings.DNS_PORT, protocol)
    reactor.listenTCP(settings.DNS_PORT, factory)

    reactor.run()


if __name__ == '__main__':
    raise SystemExit(main())
