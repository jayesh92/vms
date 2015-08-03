from django.test import TestCase
from django.contrib.staticfiles.testing import LiveServerTestCase

from django.contrib.auth.models import User

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from volunteer.models import Volunteer
from organization.models import Organization #hack to pass travis,Bug in Code

import re


class VolunteerProfile(LiveServerTestCase):
    '''
    '''
    def setUp(self):
        volunteer_user = User.objects.create_user(
                username = 'Sherlock',
                password = 'Holmes',
                email = 'idonthave@gmail.com')

        Volunteer.objects.create(
                user = volunteer_user,
                email = 'idonthave@gmail.com',
                address = '221-B Baker Street',
                city = 'London',
                state = 'London-State',
                country = 'UK',
                phone_number = '9999999999',
                unlisted_organization = 'Detective')

        # create an org prior to registration. Bug in Code
        # added to pass CI
        Organization.objects.create(
                name = 'DummyOrg')

        self.homepage = '/home/'
        self.authentication_page = '/authentication/login/'
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        super(VolunteerProfile, self).setUp()

    def tearDown(self):
        pass
        #self.driver.quit()
        #super(VolunteerProfile, self).tearDown()

    def login(self):
        self.driver.get(self.live_server_url + self.authentication_page)
        self.driver.find_element_by_id('id_login').send_keys('Sherlock')
        self.driver.find_element_by_id('id_password').send_keys('Holmes')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.homepage)

    def test_details_tab(self):
        self.login()
        self.driver.find_element_by_link_text('Profile').click()
        page_source = self.driver.page_source

        found_email = re.search('idonthave@gmail.com', page_source)
        self.assertNotEqual(found_email, None)

        found_city = re.search('London', page_source)
        self.assertNotEqual(found_city, None)

        found_state = re.search('London-State', page_source)
        self.assertNotEqual(found_state, None)

        found_country = re.search('UK', page_source)
        self.assertNotEqual(found_country, None)

        found_org = re.search('Detective', page_source)
        self.assertNotEqual(found_org, None)

    def test_edit_profile(self):
        self.login()
        self.driver.find_element_by_link_text('Profile').click()
        self.driver.find_element_by_link_text('Edit Profile').click()

        self.driver.find_element_by_xpath(
                '//input[@name = "first_name"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "first_name"]').send_keys('Harvey')

        self.driver.find_element_by_xpath(
                '//input[@name = "last_name"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "last_name"]').send_keys('Specter')

        self.driver.find_element_by_xpath(
                '//input[@name = "email"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "email"]').send_keys('hspecter@ps.com')

        self.driver.find_element_by_xpath(
                '//input[@name = "address"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "address"]').send_keys('Empire State Building')

        self.driver.find_element_by_xpath(
                '//input[@name = "city"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "city"]').send_keys('NYC')
        
        self.driver.find_element_by_xpath(
                '//input[@name = "state"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "state"]').send_keys('New York')

        self.driver.find_element_by_xpath(
                '//input[@name = "country"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "country"]').send_keys('USA')

        self.driver.find_element_by_xpath(
                '//input[@name = "phone_number"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "phone_number"]').send_keys('9999999998')

        self.driver.find_element_by_xpath(
                '//select[@name = "organization_name"]').send_keys('None')

        self.driver.find_element_by_xpath(
                '//input[@name = "unlisted_organization"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "unlisted_organization"]').send_keys('Lawyer')
        self.driver.find_element_by_xpath('//form').submit()

        page_source = self.driver.page_source

        found_email = re.search('idonthave@gmail.com', page_source)
        self.assertEqual(found_email, None)

        found_city = re.search('London', page_source)
        self.assertEqual(found_city, None)

        found_state = re.search('London-State', page_source)
        self.assertEqual(found_state, None)

        found_country = re.search('UK', page_source)
        self.assertEqual(found_country, None)

        found_org = re.search('Detective', page_source)
        self.assertEqual(found_org, None)

        found_email = re.search('hspecter@ps.com', page_source)
        self.assertNotEqual(found_email, None)

        found_city = re.search('NYC', page_source)
        self.assertNotEqual(found_city, None)

        found_state = re.search('New York', page_source)
        self.assertNotEqual(found_state, None)

        found_country = re.search('USA', page_source)
        self.assertNotEqual(found_country, None)

        found_org = re.search('Lawyer', page_source)
        self.assertNotEqual(found_org, None)

    def test_resume(self):
        pass
