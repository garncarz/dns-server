from django.test import TestCase
from twisted.names import dns, error

from dns.networking import Resolver
from dns import models


class NetworkingTestCase(TestCase):

    test_ip = '1.2.3.4'
    test_name = 'home.mydomain.org'

    def setUp(self):
        self.resolver = Resolver()

    def test_resolve(self):
        models.Record.objects.create(ip=self.test_ip, name=self.test_name)
        
        # Test synchronously since defer.succeed() is immediately available
        deferred = self.resolver.query(dns.Query(name=self.test_name))
        
        # Since this returns defer.succeed(), we can get the result immediately
        result = deferred.result
        answers, authority, additional = result
        self.assertEqual(answers[0].payload.dottedQuad(), self.test_ip)

    def test_no_resolve(self):
        deferred = self.resolver.query(dns.Query(name=self.test_name))
        
        # Since this returns defer.fail(), we can get the failure immediately
        result = deferred.result
        self.assertIsInstance(result.value, error.DomainError)
