from django.test import TestCase
from .zabbix.api import Zabbix
from django.conf import settings


class TestZabbix(TestCase):

    def test_zabbix_auth(self):
        zp = Zabbix(settings.ZABBIX_USER, settings.ZABBIX_PASSWORD)
        self.assertTrue(len(zp.api_token) == 32)
