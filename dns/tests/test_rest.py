from constance import config
from constance.test import override_config
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from dns import models


ADMIN_LOGIN = 'admin'
ADMIN_EMAIL = '%s@mydomain.org' % ADMIN_LOGIN
ADMIN_PASSWORD = 'kejh2k3hr24w'

USER_LOGIN = 'user'
USER_PASSWORD = 'sdfvu43re2'


@override_config(DOMAIN='mydomain.org')
class RestTestCase(APITestCase):

    test_ip = '1.2.3.4'
    test_name = 'home.%s' % config.DOMAIN

    def setUp(self):
        self.admin = User.objects.create_superuser(username=ADMIN_LOGIN,
                                                   email=ADMIN_EMAIL,
                                                   password=ADMIN_PASSWORD)
        self.user = User.objects.create_user(username=USER_LOGIN,
                                             password=USER_PASSWORD)

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

    def test_user_add(self):
        self.client.login(username=USER_LOGIN, password=USER_PASSWORD)
        name = '%s.%s' % (USER_LOGIN, config.DOMAIN)
        response = self.client.post(
            reverse('dns:api:record-list'),
            {'ip': self.test_ip, 'name': name}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(1, models.Record.objects.filter(ip=self.test_ip,
                                                         name=name)
                            .count())

    def test_user_add_auto(self):
        self.client.login(username=USER_LOGIN, password=USER_PASSWORD)
        ip = '3.42.7.1'
        response = self.client.post(
            reverse('dns:api:record-list'),
            {'ip': 'auto'},
            REMOTE_ADDR=ip,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        rec = models.Record.objects.last()
        self.assertEqual(rec.name, '%s.%s' % (USER_LOGIN, config.DOMAIN))
        self.assertEqual(rec.ip, ip)

    def test_user_add_auto_behind_proxy(self):
        self.client.login(username=USER_LOGIN, password=USER_PASSWORD)
        real_ip = '11.2.36.8'
        proxy_ip = '101.99.0.6'
        response = self.client.post(
            reverse('dns:api:record-list'),
            {'ip': 'auto'},
            REMOTE_ADDR=proxy_ip,
            HTTP_X_FORWARDED_FOR='%s,%s' % (real_ip, proxy_ip),
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        rec = models.Record.objects.last()
        self.assertEqual(rec.name, '%s.%s' % (USER_LOGIN, config.DOMAIN))
        self.assertEqual(rec.ip, real_ip)

    def test_user_add_fail(self):
        self.client.login(username=USER_LOGIN, password=USER_PASSWORD)
        response = self.client.post(
            reverse('dns:api:record-list'),
            {'ip': self.test_ip, 'name': self.test_name}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(0, models.Record.objects.filter(ip=self.test_ip,
                                                         name=self.test_name)
                            .count())

    def test_user_update_auto(self):
        self.test_user_add_auto()
        rec = models.Record.objects.last()

        ip2 = '3.42.7.11'
        response = self.client.post(
            reverse('dns:api:record-list'),
            {'ip': 'auto'},
            REMOTE_ADDR=ip2,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        rec.refresh_from_db()
        self.assertEqual(rec.name, '%s.%s' % (USER_LOGIN, config.DOMAIN))
        self.assertEqual(rec.ip, ip2)

    def test_anonym_cannot_add(self):
        response = self.client.post(
            reverse('dns:api:record-list'),
            {'ip': self.test_ip, 'name': self.test_name}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(0, models.Record.objects.filter(ip=self.test_ip,
                                                         name=self.test_name)
                            .count())

    def test_anonym_cannot_see_list(self):
        response = self.client.get(reverse('dns:api:record-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
