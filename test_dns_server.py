from twisted.names import dns, error
from twisted.trial import unittest

from dns_server import MyResolver
from dns import models


class TwistedTestCase(unittest.TestCase):

    test_ip = '1.2.3.4'
    test_name = 'home.mydomain.org'

    def setUp(self):
        self.resolver = MyResolver()

    def test_resolve(self):
        models.Record.objects.create(ip=self.test_ip, name=self.test_name)
        response = self.resolver.query(dns.Query(name=self.test_name))
        self.assertEqual(response.result[0][0].payload.dottedQuad(),
                         self.test_ip)

    def test_no_resolve(self):
        self.failureResultOf(
            self.resolver.query(dns.Query(name=self.test_name)),
            error.DomainError
        )
