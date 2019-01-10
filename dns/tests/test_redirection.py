from django.test import TestCase

from dns import models


class RedirectionTestCase(TestCase):

    def test_redirection(self):
        url = 'https://vietcong1.eu'
        models.Redirection.objects.create(abbr='vc', target=url)

        resp = self.client.get('/links/vc')

        self.assertRedirects(resp, url, fetch_redirect_response=False)
