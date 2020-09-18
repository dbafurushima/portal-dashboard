from django.test import TestCase
from django.test.client import Client
from django.conf import settings


class ApiTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_render_inventory_GET(self):
        response = self.client.get('/api/inventory', headers={'Authorization': f'Token {settings.USER_API_KEY}'})
        # redirect because unauthenticated users cannot see
        self.failUnlessEqual(response.status_code, 301)
