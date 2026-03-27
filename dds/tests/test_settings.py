# dds/tests/test_settings.py
from django.test import TestCase
from django.conf import settings

class SettingsTest(TestCase):
    def test_timezone(self):
        self.assertEqual(settings.TIME_ZONE, 'Europe/Moscow')
    
    def test_app_installed(self):
        self.assertIn('dds', settings.INSTALLED_APPS)