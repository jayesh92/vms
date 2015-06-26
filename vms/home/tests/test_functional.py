from django.test import TestCase
from django.contrib.staticfiles.testing import LiveServerTestCase

from django.contrib.auth.models import User

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from volunteer.models import Volunteer
from administrator.models import Administrator
from organization.models import Organization #hack to pass travis,Bug in Code

import re


class TestAccessControl(LiveServerTestCase):
    '''
    TestAccessControl class contains the functional tests to check Admin and
    Volunteer can access '/home' view of VMS. Following tests are included:
    Administrator:
        - Login admin with correct credentials
        - Login admin with incorrect credentials 
    Volunteer:
        - Login volunteer with correct credentials
        - Login volunteer with incorrect credentials 
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

        Volunteer.objects.create(
                user = volunteer_user,
                address = 'address',
                city = 'city',
                state = 'state',
                country = 'country',
                phone_number = '9999999999',
                unlisted_organization = 'organization')

        # create an org prior to registration. Bug in Code
        # added to pass CI
        Organization.objects.create(
                name = 'DummyOrg')

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
        redirected to '/home' and no errors are generated.
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
            self.driver.find_element_by_class_name('alert-danger')

    def test_incorrect_admin_credentials(self):
        '''
        Method to simulate logging in of an Invalid admin user and check if
        they are displayed an error and redirected to login page again.
        '''
        self.driver.get(self.live_server_url + self.homepage)
        self.driver.find_element_by_link_text('Log In').click()

        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.authentication_page)

        self.driver.find_element_by_id('id_login').send_keys('admin')
        self.driver.find_element_by_id('id_password').send_keys('wrong_password')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertNotEqual(self.driver.current_url, self.live_server_url +
                self.homepage)

        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.authentication_page)

        self.assertNotEqual(self.driver.find_element_by_class_name(
            'alert-danger'), None)

    def test_correct_volunteer_credentials(self):
        '''
        Method to simulate logging in of a valid volunteer user and check if
        they are redirected to '/home'
        '''
        self.driver.get(self.live_server_url + self.homepage)
        self.driver.find_element_by_link_text('Log In').click()

        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.authentication_page)

        self.driver.find_element_by_id('id_login').send_keys('volunteer')
        self.driver.find_element_by_id('id_password').send_keys('volunteer')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.homepage)

        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name('alert-danger')

    def test_incorrect_volunteer_credentials(self):
        '''
        Method to simulate logging in of a Invalid volunteer user and check if
        they are displayed an error and redirected to login page again.
        '''
        self.driver.get(self.live_server_url + self.homepage)
        self.driver.find_element_by_link_text('Log In').click()

        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.authentication_page)

        self.driver.find_element_by_id('id_login').send_keys('volunteer')
        self.driver.find_element_by_id('id_password').send_keys('wrong_password')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertNotEqual(self.driver.current_url, self.live_server_url +
                self.homepage)

        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.authentication_page)

        self.assertNotEqual(self.driver.find_element_by_class_name(
            'alert-danger'), None)


class CheckURLAccess(LiveServerTestCase):
    '''
    CheckURLAccess contains methods to browse(via URL) a volunteer page view
    after logging in from an admin account and vice-versa. Tests included:
    - Admin cannot access volunteer URL's
    - Volunteer cannot access admin URL's
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

        Volunteer.objects.create(
                user = volunteer_user,
                address = 'address',
                city = 'city',
                state = 'state',
                country = 'country',
                phone_number = '9999999999',
                unlisted_organization = 'organization')

        self.authentication_page = '/authentication/login/'
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        super(CheckURLAccess, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(CheckURLAccess, self).tearDown()

    def test_admin_cannot_access_volunteer_urls(self):
        '''
        Method logins an admin user and tries to surf volunteer pages through
        url. The volunteer views should return a 403 error to deny access.
        '''
        self.driver.get(self.live_server_url + self.authentication_page)

        self.driver.find_element_by_id('id_login').send_keys('admin')
        self.driver.find_element_by_id('id_password').send_keys('admin')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.driver.get(self.live_server_url +
                '/shift/view_volunteer_shifts/1')
        page_source = self.driver.page_source
        error = re.search('403', page_source)
        self.assertNotEqual(error, None)

        self.driver.get(self.live_server_url + '/shift/view_hours/1')
        page_source = self.driver.page_source
        error = re.search('403', page_source)
        self.assertNotEqual(error, None)

        self.driver.get(self.live_server_url + '/event/list_sign_up/1')
        page_source = self.driver.page_source
        error = re.search('403', page_source)
        self.assertNotEqual(error, None)

        self.driver.get(self.live_server_url + '/volunteer/report/1')
        page_source = self.driver.page_source
        error = re.search('403', page_source)
        self.assertNotEqual(error, None)

        self.driver.get(self.live_server_url + '/volunteer/profile/1')
        page_source = self.driver.page_source
        error = re.search('403', page_source)
        self.assertNotEqual(error, None)

    def test_volunteer_cannot_access_admin_urls(self):
        '''
        Method logins a volunteer and tries to surf admin page views through url.
        The admin views should return a 403 error to deny access.
        '''
        self.driver.get(self.live_server_url + self.authentication_page)

        self.driver.find_element_by_id('id_login').send_keys('volunteer')
        self.driver.find_element_by_id('id_password').send_keys('volunteer')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.driver.get(self.live_server_url + '/volunteer/search/')
        page_source = self.driver.page_source
        error = re.search('403', page_source)
        self.assertNotEqual(error, None)

        self.driver.get(self.live_server_url + '/shift/volunteer_search/')
        page_source = self.driver.page_source
        error = re.search('403', page_source)
        self.assertNotEqual(error, None)

        self.driver.get(self.live_server_url + '/administrator/report/')
        page_source = self.driver.page_source
        error = re.search('403', page_source)
        self.assertNotEqual(error, None)

        self.driver.get(self.live_server_url + '/administrator/settings/')
        page_source = self.driver.page_source
        error = re.search('403', page_source)
        self.assertNotEqual(error, None)

        self.driver.get(self.live_server_url +
                '/registration/signup_administrator/')
        page_source = self.driver.page_source
        error = re.search('403', page_source)
        self.assertNotEqual(error, None)


class CheckPageContent(LiveServerTestCase):
    '''
    This Class contains methods to check if an administrator or a volunteer
    are provided their respective views links on their dashboard.
    - Check admin page content
    - check volunteer page content
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

        Volunteer.objects.create(
                user = volunteer_user,
                address = 'address',
                city = 'city',
                state = 'state',
                country = 'country',
                phone_number = '9999999999',
                unlisted_organization = 'organization')

        self.authentication_page = '/authentication/login/'
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        super(CheckPageContent, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(CheckPageContent, self).tearDown()

    def test_check_admin_page_content(self):
        '''
        Check if an admin user has following functionalities on its home page.
        - Volunteer Search
        - Manage Volunteer Shift
        - Report
        - Settings
        - Create Admin Account
        '''
        self.driver.get(self.live_server_url + self.authentication_page)

        self.driver.find_element_by_id('id_login').send_keys('admin')
        self.driver.find_element_by_id('id_password').send_keys('admin')
        self.driver.find_element_by_xpath('//form[1]').submit()

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

    def test_check_volunteer_page_content(self):
        '''
        Check if a volunteer user has following functionalities on its home
        page.
        - UpComing Shift
        - Shift Hours
        - Shift Sign Up
        - Report
        - Profile
        '''
        self.driver.get(self.live_server_url + self.authentication_page)

        self.driver.find_element_by_id('id_login').send_keys('volunteer')
        self.driver.find_element_by_id('id_password').send_keys('volunteer')
        self.driver.find_element_by_xpath('//form[1]').submit()

        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_link_text('Log In')

        self.assertNotEqual(self.driver.find_element_by_link_text(
            'Upcoming Shifts'), None)
        self.assertNotEqual(self.driver.find_element_by_link_text(
            'Shift Hours'), None)
        self.assertNotEqual(self.driver.find_element_by_link_text(
            'Shift Sign Up'), None)
        self.assertNotEqual(self.driver.find_element_by_link_text(
            'Report'), None)
        self.assertNotEqual(self.driver.find_element_by_link_text(
            'Profile'), None)
        self.assertNotEqual(self.driver.find_element_by_link_text(
            'Log Out'), None)
