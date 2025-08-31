from constance.test import override_config
from django.urls import reverse
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
class PastebinTestCase(APITestCase):

    def setUp(self):
        # Create superuser
        self.admin = User.objects.create_superuser(
            username=ADMIN_LOGIN,
            email=ADMIN_EMAIL,
            password=ADMIN_PASSWORD
        )
        
        # Create regular user
        self.user = User.objects.create_user(
            username=USER_LOGIN,
            password=USER_PASSWORD
        )

    def test_anonymous_can_create_pastebin(self):
        """Anonymous users should be able to create pastebins"""
        response = self.client.post(
            reverse('dns:api:pastebin-list'),
            {'content': 'This is a test snippet', 'filename': 'test.txt'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('key', response.data)
        
        # Verify the pastebin was created
        pastebin = models.Pastebin.objects.get(key=response.data['key'])
        self.assertEqual(pastebin.content, 'This is a test snippet')
        self.assertEqual(pastebin.filename, 'test.txt')

    def test_anonymous_cannot_list_pastebins(self):
        """Anonymous users should not be able to list pastebins"""
        response = self.client.get(reverse('dns:api:pastebin-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_cannot_retrieve_pastebin(self):
        """Anonymous users should not be able to retrieve specific pastebins"""
        # Create a pastebin first
        pastebin = models.Pastebin.objects.create(
            key='test-key', 
            content='test content'
        )
        
        response = self.client.get(
            reverse('dns:api:pastebin-detail', kwargs={'key': pastebin.key})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_list_pastebins(self):
        """Regular authenticated users should not be able to list pastebins"""
        self.client.login(username=USER_LOGIN, password=USER_PASSWORD)
        response = self.client.get(reverse('dns:api:pastebin-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_list_pastebins(self):
        """Admin users should be able to list pastebins"""
        # Create a pastebin first
        models.Pastebin.objects.create(
            key='test-key',
            content='test content'
        )
        
        self.client.login(username=ADMIN_LOGIN, password=ADMIN_PASSWORD)
        response = self.client.get(reverse('dns:api:pastebin-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_admin_can_retrieve_pastebin(self):
        """Admin users should be able to retrieve specific pastebins"""
        pastebin = models.Pastebin.objects.create(
            key='test-key',
            content='test content',
            filename='test.txt'
        )
        
        self.client.login(username=ADMIN_LOGIN, password=ADMIN_PASSWORD)
        response = self.client.get(
            reverse('dns:api:pastebin-detail', kwargs={'key': pastebin.key})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'test content')
        self.assertEqual(response.data['filename'], 'test.txt')

    def test_pastebin_key_uniqueness(self):
        """Each pastebin should have a unique key"""
        response1 = self.client.post(
            reverse('dns:api:pastebin-list'),
            {'content': 'First snippet'}
        )
        response2 = self.client.post(
            reverse('dns:api:pastebin-list'),
            {'content': 'Second snippet'}
        )
        
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response1.data['key'], response2.data['key'])
        
    def test_pastebin_client_ip_capture(self):
        """Pastebins should capture client IP"""
        response = self.client.post(
            reverse('dns:api:pastebin-list'),
            {'content': 'Test with IP'},
            REMOTE_ADDR='192.168.1.100'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        pastebin = models.Pastebin.objects.get(key=response.data['key'])
        self.assertEqual(pastebin.client_ip, '192.168.1.100')