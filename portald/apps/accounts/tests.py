from django.test import TestCase
from django.test.client import Client


class LoginTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_render_GET(self):
        response = self.client.get('/accounts/sign-in')
        self.failUnlessEqual(response.status_code, 200)

    def test_login_POST(self):
        response = self.client.post('/accounts/sign-in', {'username': 'user', 'password': 'user'})
        self.failUnlessEqual(response.status_code, 302)
        
    def test_login_without_parameter_POST(self):
        response = self.client.post('/accounts/sign-in', {})
        self.failUnlessEqual(response.status_code, 200)
