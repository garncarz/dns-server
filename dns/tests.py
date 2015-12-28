from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from . import models


ADMIN_LOGIN = 'admin'
ADMIN_EMAIL = '%s@mydomain.org' % ADMIN_LOGIN
ADMIN_PASSWORD = 'kejh2k3hr24w'


class RestTestCase(APITestCase):

    test_ip = '1.2.3.4'
    test_name = 'home.domain.org'

    def setUp(self):
        self.admin = User.objects.create_superuser(username=ADMIN_LOGIN,
                                                   email=ADMIN_EMAIL,
                                                   password=ADMIN_PASSWORD)

    def test_add(self):
        self.client.login(username=ADMIN_LOGIN, password=ADMIN_PASSWORD)
        response = self.client.post(
            reverse('dns:api:record-list'),
            {'ip': self.test_ip, 'name': self.test_name}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(1, models.Record.objects.filter(ip=self.test_ip,
                                                     name=self.test_name)
                            .count())

    def test_anonym_cannot_add(self):
        response = self.client.post(
            reverse('dns:api:record-list'),
            {'ip': self.test_ip, 'name': self.test_name}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(0, models.Record.objects.filter(ip=self.test_ip,
                                                     name=self.test_name)
                            .count())
