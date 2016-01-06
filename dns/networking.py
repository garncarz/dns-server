from django.conf import settings
from twisted.internet import reactor, defer
from twisted.names import client, dns, error, server

from models import Record


class Resolver(object):
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


def run():
    clients = [Resolver()]
    if settings.DNS_RELAY:
        clients.append(client.Resolver(resolv='/etc/resolv.conf'))

    factory = server.DNSServerFactory(clients=clients)
    protocol = dns.DNSDatagramProtocol(controller=factory)

    reactor.listenUDP(settings.DNS_PORT, protocol)
    reactor.listenTCP(settings.DNS_PORT, factory)

    reactor.run()
