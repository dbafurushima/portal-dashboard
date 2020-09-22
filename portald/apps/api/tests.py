import json
import requests
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

        raw_data = json.loads(requests.get('http://localhost:8000/api/inventory/',
                                           headers={'Authorization': f'Token {settings.USER_API_KEY}'}).text)

        self.failUnlessEqual(type(raw_data), list)
        self.assertTrue(len(raw_data) > 0)
