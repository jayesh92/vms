from django.test import TestCase
from django.contrib.staticfiles.testing import LiveServerTestCase

from django.contrib.auth.models import User

from selenium import webdriver

class AdminTestCase(LiveServerTestCase):
    def setUp(self):
        User.objects.create_superuser(
                username = 'admin',
                password = 'admin',
                email = 'admin@admin.com'
                )

        self.selenium = webdriver.Firefox()
        self.selenium.maximize_window()
        super(AdminTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(AdminTestCase, self).tearDown()

    def test_admin_site(self):
        pass
