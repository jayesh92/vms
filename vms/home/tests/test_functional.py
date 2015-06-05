from django.test import TestCase
from django.contrib.staticfiles.testing import LiveServerTestCase

from django.contrib.auth.models import User

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from volunteer.models import Volunteer
from administrator.models import Administrator


class TestAccessControl(LiveServerTestCase):
    '''
    This class contains the functional tests to check Admin and Volunteer access
    control to '/home' view of VMS.
    '''
    def setUp(self):
        admin_user = User.objects.create_user(
                username = 'admin',
                password = 'admin',
                email = 'admin@admin.com')

        volunteer_user = User.objects.create_user(
                username = 'volunteer',
                password = 'volunteer',
                email = 'volunteer@volunteer.com')

        Administrator.objects.create(
                user = admin_user,
                address = 'address',
                city = 'city',
                state = 'state',
                country = 'country',
                phone_number = '9999999999',
                unlisted_organization = 'organization')

        self.homepage = '/home/'
        self.authentication_page = '/authentication/login/'
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        super(TestAccessControl, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(TestAccessControl, self).tearDown()

    def test_correct_admin_credentials(self):
        '''
        Method to simulate logging in of a valid admin user and check if they
        are NOT displayed any error as well as displayed all admin
        functionality after redirecting to '/home'
        '''
        self.driver.get(self.live_server_url + self.homepage)
        self.driver.find_element_by_link_text('Log In').click()

        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.authentication_page)

        self.driver.find_element_by_id('id_login').send_keys('admin')
        self.driver.find_element_by_id('id_password').send_keys('admin')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.homepage)

        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_link_text('Log In')

        self.assertNotEqual(self.driver.find_element_by_link_text(
            'Volunteer Search'), None)
        self.assertNotEqual(self.driver.find_element_by_link_text(
            'Manage Volunteer Shifts'), None)
        self.assertNotEqual(self.driver.find_element_by_link_text(
            'Report'), None)
        self.assertNotEqual(self.driver.find_element_by_link_text(
            'Settings'), None)
        self.assertNotEqual(self.driver.find_element_by_link_text(
            'Create Admin Account'), None)
        self.assertNotEqual(self.driver.find_element_by_link_text(
            'Log Out'), None)

    def test_incorrect_admin_credentials(self):
        '''
        Method to simulate logging in of a Invalid admin user and check if they
        are displayed an error and redirected to login page again.
        '''
        self.driver.get(self.live_server_url + self.homepage)
        self.driver.find_element_by_link_text('Log In').click()

        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.authentication_page)

        self.driver.find_element_by_id('id_login').send_keys('admin')
        self.driver.find_element_by_id('id_password').send_keys('admin1')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertNotEqual(self.driver.current_url, self.live_server_url +
                self.homepage)

        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.authentication_page)

        self.assertNotEqual(self.driver.find_element_by_class_name(
            'alert-danger'), None)
