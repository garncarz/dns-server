import logging

from django.conf import settings
from django_statsd.clients import statsd
from twisted.internet import reactor, defer
from twisted.names import client, dns, error, server

from .models import Record

logger = logging.getLogger(__name__)


class Resolver(object):
    def query(self, query, timeout=None):
        # Log all incoming DNS queries for debugging
        try:
            logger.info('Received DNS query: %s', query)
            logger.debug('Query details - type: %s, class: %s', 
                        getattr(query, 'type', 'unknown'), 
                        getattr(query, 'cls', 'unknown'))
            
            # Try to safely access query name
            query_name = None
            query_name_str = None
            try:
                query_name = query.name.name
                logger.debug('Query name: %s', query_name)
                # Convert bytes to string if necessary for database lookup
                if isinstance(query_name, bytes):
                    query_name_str = query_name.decode('utf-8')
                else:
                    query_name_str = str(query_name)
            except AttributeError as e:
                logger.warning('Failed to extract query name: %s, query object: %s', e, query)
                return defer.fail(error.DomainError())
            except Exception as e:
                logger.error('Unexpected error accessing query name: %s, query object: %s', e, query)
                return defer.fail(error.DomainError())
            
            # Look up the record
            try:
                rec = Record.objects.get(name=query_name_str)
                logger.debug('Responding with %s' % rec)
                statsd.incr('record.get')

                answer = dns.RRHeader(
                    name=query_name,
                    payload=dns.Record_A(address=rec.ip),
                )
                answers = [answer]
                authority = []
                additional = []

                return defer.succeed((answers, authority, additional))
            
            except Record.DoesNotExist:
                logger.info('No record found for query name: %s', query_name_str)
                return defer.fail(error.DomainError())
                
        except Exception as e:
            logger.error('Unhandled error in DNS query processing: %s, query object: %s', e, query)
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
