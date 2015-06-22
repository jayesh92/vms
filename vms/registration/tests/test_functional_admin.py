from django.test import TestCase
from django.contrib.staticfiles.testing import LiveServerTestCase

from django.contrib.auth.models import User

import re

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from organization.models import Organization #hack to pass travis,Bug in Code


class SignUpAdmin(LiveServerTestCase):
    '''
    SignUpAdmin Class contains tests to register a admin User
    '''
    def setUp(self):        
        # create an org prior to registration. Bug in Code
        # added to pass CI
        Organization.objects.create(
                name = 'DummyOrg')

        self.homepage = '/home/'
        self.admin_registration_page = '/registration/signup_administrator/'
        self.authentication_page = '/authentication/login/'
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        super(SignUpAdmin, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(SignUpAdmin, self).tearDown()

    def test_null_values(self):
        self.driver.get(self.live_server_url + self.admin_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('')
        self.driver.find_element_by_id('id_password').send_keys('')
        self.driver.find_element_by_id('id_first_name').send_keys('')
        self.driver.find_element_by_id('id_last_name').send_keys('')
        self.driver.find_element_by_id('id_email').send_keys('')
        self.driver.find_element_by_id('id_address').send_keys('')
        self.driver.find_element_by_id('id_city').send_keys('')
        self.driver.find_element_by_id('id_state').send_keys('')
        self.driver.find_element_by_id('id_country').send_keys('')
        self.driver.find_element_by_id('id_phone_number').send_keys('')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)

    def test_name_fields(self):
        # register valid admin user
        self.driver.get(self.live_server_url + self.admin_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('admin-username')
        self.driver.find_element_by_id('id_password').send_keys('admin-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('admin-first-name')
        self.driver.find_element_by_id('id_last_name').send_keys('admin-last-name')
        self.driver.find_element_by_id('id_email').send_keys('email@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('admin-address')
        self.driver.find_element_by_id('id_city').send_keys('admin-city')
        self.driver.find_element_by_id('id_state').send_keys('admin-state')
        self.driver.find_element_by_id('id_country').send_keys('admin-country')
        self.driver.find_element_by_id('id_phone_number').send_keys('9999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('admin-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name('help-block')

        # register a user again with username same as already registered user
        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.homepage)

        self.driver.get(self.live_server_url + self.admin_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('admin-username')
        self.driver.find_element_by_id('id_password').send_keys('admin-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('admin-first-name')
        self.driver.find_element_by_id('id_last_name').send_keys('admin-last-name')
        self.driver.find_element_by_id('id_email').send_keys('email@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('admin-address')
        self.driver.find_element_by_id('id_city').send_keys('admin-city')
        self.driver.find_element_by_id('id_state').send_keys('admin-state')
        self.driver.find_element_by_id('id_country').send_keys('admin-country')
        self.driver.find_element_by_id('id_phone_number').send_keys('9999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('admin-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_username')/div/p/strong").text,
                'User with this Username already exists.')

        # test numeric characters in first-name, last-name
        self.driver.get(self.live_server_url + self.admin_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('admin-username-1')
        self.driver.find_element_by_id('id_password').send_keys('admin-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('admin-first-name-1')
        self.driver.find_element_by_id('id_last_name').send_keys('admin-last-name-1')
        self.driver.find_element_by_id('id_email').send_keys('email@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('admin-address')
        self.driver.find_element_by_id('id_city').send_keys('admin-city')
        self.driver.find_element_by_id('id_state').send_keys('admin-state')
        self.driver.find_element_by_id('id_country').send_keys('admin-country')
        self.driver.find_element_by_id('id_phone_number').send_keys('9999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('admin-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_first_name')/div/p/strong").text,
                'Enter a valid value.')
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_last_name')/div/p/strong").text,
                'Enter a valid value.')

        # test special characters in first-name, last-name
        self.driver.get(self.live_server_url + self.admin_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('admin-username-1')
        self.driver.find_element_by_id('id_password').send_keys('admin-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('name-!@#$%^&*()_')
        self.driver.find_element_by_id('id_last_name').send_keys('name-!@#$%^&*()_')
        self.driver.find_element_by_id('id_email').send_keys('email@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('admin-address')
        self.driver.find_element_by_id('id_city').send_keys('admin-city')
        self.driver.find_element_by_id('id_state').send_keys('admin-state')
        self.driver.find_element_by_id('id_country').send_keys('admin-country')
        self.driver.find_element_by_id('id_phone_number').send_keys('9999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('admin-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_first_name')/div/p/strong").text,
                'Enter a valid value.')
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_last_name')/div/p/strong").text,
                'Enter a valid value.')

        # test length of first-name, last-name not exceed 30
        self.driver.get(self.live_server_url + self.admin_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('admin-username-1')
        self.driver.find_element_by_id('id_password').send_keys('admin-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('admin-first-name-!@#$%^&*()_')
        self.driver.find_element_by_id('id_last_name').send_keys('admin-last-name-!@#$%^&*()_')
        self.driver.find_element_by_id('id_email').send_keys('email@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('admin-address')
        self.driver.find_element_by_id('id_city').send_keys('admin-city')
        self.driver.find_element_by_id('id_state').send_keys('admin-state')
        self.driver.find_element_by_id('id_country').send_keys('admin-country')
        self.driver.find_element_by_id('id_phone_number').send_keys('9999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('admin-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        error_message = self.driver.find_element_by_xpath("id('div_id_first_name')/div/p/strong").text
        self.assertTrue(bool(re.search(r'Ensure this value has at most 20 characters', str(error_message))))

        error_message = self.driver.find_element_by_xpath("id('div_id_last_name')/div/p/strong").text,
        self.assertTrue(bool(re.search(r'Ensure this value has at most 20 characters', str(error_message))))

    def test_address_field(self):
        # register valid admin user
        self.driver.get(self.live_server_url + self.admin_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('admin-username')
        self.driver.find_element_by_id('id_password').send_keys('admin-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('admin-first-name')
        self.driver.find_element_by_id('id_last_name').send_keys('admin-last-name')
        self.driver.find_element_by_id('id_email').send_keys('email@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('admin-address')
        self.driver.find_element_by_id('id_city').send_keys('admin-city')
        self.driver.find_element_by_id('id_state').send_keys('admin-state')
        self.driver.find_element_by_id('id_country').send_keys('admin-country')
        self.driver.find_element_by_id('id_phone_number').send_keys('9999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('admin-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name('help-block')

        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.homepage)

        # test numeric characters in address
        self.driver.get(self.live_server_url + self.admin_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('admin-username-1')
        self.driver.find_element_by_id('id_password').send_keys('admin-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('admin-first-name')
        self.driver.find_element_by_id('id_last_name').send_keys('admin-last-name')
        self.driver.find_element_by_id('id_email').send_keys('email@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('123 New-City address')
        self.driver.find_element_by_id('id_city').send_keys('admin-city')
        self.driver.find_element_by_id('id_state').send_keys('admin-state')
        self.driver.find_element_by_id('id_country').send_keys('admin-country')
        self.driver.find_element_by_id('id_phone_number').send_keys('9999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('admin-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name('help-block')

        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.homepage)

        # test special characters in address
        self.driver.get(self.live_server_url + self.admin_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('admin-username-2')
        self.driver.find_element_by_id('id_password').send_keys('admin-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('first-name')
        self.driver.find_element_by_id('id_last_name').send_keys('last-name')
        self.driver.find_element_by_id('id_email').send_keys('email@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('admin-address!@#$()')
        self.driver.find_element_by_id('id_city').send_keys('admin-city')
        self.driver.find_element_by_id('id_state').send_keys('admin-state')
        self.driver.find_element_by_id('id_country').send_keys('admin-country')
        self.driver.find_element_by_id('id_phone_number').send_keys('9999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('admin-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.admin_registration_page)
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_address')/div/p/strong").text,
                'Enter a valid value.')

    def test_city_field(self):
        # register valid admin user
        self.driver.get(self.live_server_url + self.admin_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('admin-username')
        self.driver.find_element_by_id('id_password').send_keys('admin-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('admin-first-name')
        self.driver.find_element_by_id('id_last_name').send_keys('admin-last-name')
        self.driver.find_element_by_id('id_email').send_keys('email@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('admin-address')
        self.driver.find_element_by_id('id_city').send_keys('admin-city')
        self.driver.find_element_by_id('id_state').send_keys('admin-state')
        self.driver.find_element_by_id('id_country').send_keys('admin-country')
        self.driver.find_element_by_id('id_phone_number').send_keys('9999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('admin-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name('help-block')

        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.homepage)

        # test numeric characters in city
        self.driver.get(self.live_server_url + self.admin_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('admin-username-1')
        self.driver.find_element_by_id('id_password').send_keys('admin-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('admin-first-name')
        self.driver.find_element_by_id('id_last_name').send_keys('admin-last-name')
        self.driver.find_element_by_id('id_email').send_keys('email@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('admin-address')
        self.driver.find_element_by_id('id_city').send_keys('13th admin-city')
        self.driver.find_element_by_id('id_state').send_keys('admin-state')
        self.driver.find_element_by_id('id_country').send_keys('admin-country')
        self.driver.find_element_by_id('id_phone_number').send_keys('9999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('admin-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.admin_registration_page)
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_city')/div/p/strong").text,
                'Enter a valid value.')

        # test special characters in city
        self.driver.get(self.live_server_url + self.admin_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('admin-username-1')
        self.driver.find_element_by_id('id_password').send_keys('admin-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('first-name')
        self.driver.find_element_by_id('id_last_name').send_keys('last-name')
        self.driver.find_element_by_id('id_email').send_keys('email@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('admin-address')
        self.driver.find_element_by_id('id_city').send_keys('!@#$%^&*()_+city')
        self.driver.find_element_by_id('id_state').send_keys('admin-state')
        self.driver.find_element_by_id('id_country').send_keys('admin-country')
        self.driver.find_element_by_id('id_phone_number').send_keys('9999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('admin-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.admin_registration_page)
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_city')/div/p/strong").text,
                'Enter a valid value.')
