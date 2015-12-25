#!/usr/bin/env python2

from twisted.internet import reactor, defer
from twisted.names import client, dns, error, server

MY_DOMAIN = 'dyndns.mydomain.org'
DNS_PORT = 10053


class MyResolver(object):
    def _should_resolve(self, query):
        if query.type == dns.A:
            if query.name.name.endswith(MY_DOMAIN):
                return True
        return False

    def _resolve(self, query):
        name = query.name.name
        answer = dns.RRHeader(
            name=name,
            payload=dns.Record_A(address=b'1.2.3.4'),
        )
        answers = [answer]
        authority = []
        additional = []
        return answers, authority, additional

    def query(self, query, timeout=None):
        if self._should_resolve(query):
            return defer.succeed(self._resolve(query))
        else:
            return defer.fail(error.DomainError())


def main():
    factory = server.DNSServerFactory(
        clients=[MyResolver(),
                 client.Resolver(resolv='/etc/resolv.conf')]
    )
    protocol = dns.DNSDatagramProtocol(controller=factory)

    reactor.listenUDP(DNS_PORT, protocol)
    reactor.listenTCP(DNS_PORT, factory)

    reactor.run()


if __name__ == '__main__':
    raise SystemExit(main())
