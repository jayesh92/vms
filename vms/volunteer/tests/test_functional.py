from django.test import TestCase
from django.contrib.staticfiles.testing import LiveServerTestCase

from django.contrib.auth.models import User

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from administrator.models import Administrator
from organization.models import Organization #hack to pass travis,Bug in Code

class SearchVolunteer(LiveServerTestCase):
    '''
    SearchVolunteer class contains tests to check '/voluneer/search/' view.
    Choices of parameters contains
    - First Name
    - Last Name
    - City
    - State
    - Country
    - Organization
    Class contains 7 tests to check each parameter separately and also to check
    if a combination of parameters entered, then intersection of all results is
    obtained.
    '''
    def setUp(self):
        admin_user = User.objects.create_user(
                username = 'admin',
                password = 'admin',
                email = 'admin@admin.com')

        Administrator.objects.create(
                user = admin_user,
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
        self.registration_page = '/registration/signup_volunteer/'
        self.authentication_page = '/authentication/login/'
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        super(SearchVolunteer, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(SearchVolunteer, self).tearDown()

    def register_volunteer(self,credentials):
        '''
        Utility function to register a volunteer with supplied credentials.
        Credentials is a list of parameters to register a volunteer. Parameters
        are in following order.
        - username
        - password
        - first_name
        - last_name
        - email
        - address
        - city
        - state
        - country
        - phone_number
        - organization
        '''
        self.driver.get(self.live_server_url + '/registration/signup_volunteer/')

        self.driver.find_element_by_id('id_username').send_keys(credentials[0])
        self.driver.find_element_by_id('id_password').send_keys(credentials[1])
        self.driver.find_element_by_id('id_first_name').send_keys(credentials[2])
        self.driver.find_element_by_id('id_last_name').send_keys(credentials[3])
        self.driver.find_element_by_id('id_email').send_keys(credentials[4])
        self.driver.find_element_by_id('id_address').send_keys(credentials[5])
        self.driver.find_element_by_id('id_city').send_keys(credentials[6])
        self.driver.find_element_by_id('id_state').send_keys(credentials[7])
        self.driver.find_element_by_id('id_country').send_keys(credentials[8])
        self.driver.find_element_by_id('id_phone_number').send_keys(credentials[9])
        self.driver.find_element_by_id('id_unlisted_organization').send_keys(credentials[10])
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.homepage)

    def login_admin(self):
        '''
        Utility function to login an admin user to perform all tests.
        '''
        self.driver.get(self.live_server_url + self.authentication_page)
        self.driver.find_element_by_id('id_login').send_keys('admin')
        self.driver.find_element_by_id('id_password').send_keys('admin')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.homepage)

    def test_volunteer_first_name_field(self):            
        credentials = ['volunteer-username', 'volunteer-password',
                'VOLUNTEER-FIRST-NAME', 'volunteer-last-name',
                'volunteer-email@systers.org', 'volunteer-address',
                'volunteer-city', 'volunteer-state', 'volunteer-country',
                '9999999999', 'volunteer-organization']

        self.register_volunteer(credentials)

        credentials = ['volunteer-usernameq', 'volunteer-passwordq',
                'volunteer-first-name', 'volunteer-last-nameq',
                'volunteer-email@systers.orgq', 'volunteer-addressq',
                'volunteer-cityq', 'volunteer-stateq', 'volunteer-countryq',
                '9999999999', 'volunteer-organizationq']

        self.register_volunteer(credentials)
        self.login_admin()

        self.driver.find_element_by_link_text('Volunteer Search').click()
        self.assertEqual(self.driver.current_url, self.live_server_url +
                '/volunteer/search/')

        self.driver.find_element_by_css_selector(".form-control[name='first_name']").send_keys('volunteer')
        self.driver.find_element_by_tag_name('button').click()

        search_results = self.driver.find_element_by_xpath('//table//tbody')

        result = []
        for tr in search_results.find_elements_by_tag_name('tr'):
            row = tr.text.split()
            result.append(row)
        
        self.assertEqual(len(result), 2)

        expected_result = ['volunteer-first-name', 'volunteer-last-nameq',
                'volunteer-addressq', 'volunteer-cityq', 'volunteer-stateq',
                'volunteer-countryq', 'volunteer-organizationq', '9999999999',
                'volunteer-email@systers.orgq']
        
        self.assertTrue(expected_result in result)

        expected_result = ['VOLUNTEER-FIRST-NAME', 'volunteer-last-name',
                'volunteer-address', 'volunteer-city', 'volunteer-state',
                'volunteer-country', 'volunteer-organization', '9999999999',
                'volunteer-email@systers.org']

        self.assertTrue(expected_result in result)

        self.driver.find_element_by_css_selector(".form-control[name='first_name']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='first_name']").send_keys('e')
        self.driver.find_element_by_tag_name('button').click()

        self.assertEqual(len(result), 2)

        expected_result = ['volunteer-first-name', 'volunteer-last-nameq',
                'volunteer-addressq', 'volunteer-cityq', 'volunteer-stateq',
                'volunteer-countryq', 'volunteer-organizationq', '9999999999',
                'volunteer-email@systers.orgq']
        
        self.assertTrue(expected_result in result)

        expected_result = ['VOLUNTEER-FIRST-NAME', 'volunteer-last-name',
                'volunteer-address', 'volunteer-city', 'volunteer-state',
                'volunteer-country', 'volunteer-organization', '9999999999',
                'volunteer-email@systers.org']

        self.assertTrue(expected_result in result)

        self.driver.find_element_by_css_selector(".form-control[name='first_name']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='first_name']").send_keys('vol-')
        self.driver.find_element_by_tag_name('button').click()

        with self.assertRaises(NoSuchElementException):
            search_results = self.driver.find_element_by_xpath('//table//tbody')

        self.driver.find_element_by_css_selector(".form-control[name='first_name']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='first_name']").send_keys('volunteer-fail-test')
        self.driver.find_element_by_tag_name('button').click()

        with self.assertRaises(NoSuchElementException):
            search_results = self.driver.find_element_by_xpath('//table//tbody')

        self.driver.find_element_by_css_selector(".form-control[name='first_name']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='first_name']").send_keys('!@#$%^&*()_')
        self.driver.find_element_by_tag_name('button').click()
        self.assertNotEqual(self.driver.find_element_by_class_name('help-block'),
                None)

    def test_volunteer_last_name_field(self):            
        credentials = ['volunteer-username', 'volunteer-password',
                'volunteer-first-name', 'VOLUNTEER-LAST-NAME',
                'volunteer-email@systers.org', 'volunteer-address',
                'volunteer-city', 'volunteer-state', 'volunteer-country',
                '9999999999', 'volunteer-organization']

        self.register_volunteer(credentials)

        credentials = ['volunteer-usernameq', 'volunteer-passwordq',
                'volunteer-first-nameq', 'volunteer-last-name',
                'volunteer-email@systers.orgq', 'volunteer-addressq',
                'volunteer-cityq', 'volunteer-stateq', 'volunteer-countryq',
                '9999999999', 'volunteer-organizationq']

        self.register_volunteer(credentials)

        self.login_admin()
        self.driver.get(self.live_server_url + '/volunteer/search/')
        self.assertEqual(self.driver.current_url, self.live_server_url +
                '/volunteer/search/')

        self.driver.find_element_by_css_selector(".form-control[name='last_name']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='last_name']").send_keys('volunteer')
        self.driver.find_element_by_tag_name('button').click()

        search_results = self.driver.find_element_by_xpath('//table//tbody')

        result = []
        for tr in search_results.find_elements_by_tag_name('tr'):
            row = tr.text.split()
            result.append(row)

        expected_result = ['volunteer-first-nameq', 'volunteer-last-name',
                'volunteer-addressq', 'volunteer-cityq', 'volunteer-stateq',
                'volunteer-countryq', 'volunteer-organizationq', '9999999999',
                'volunteer-email@systers.orgq']
        
        self.assertTrue(expected_result in result)

        expected_result = ['volunteer-first-name', 'VOLUNTEER-LAST-NAME',
                'volunteer-address', 'volunteer-city', 'volunteer-state',
                'volunteer-country', 'volunteer-organization', '9999999999',
                'volunteer-email@systers.org']

        self.assertTrue(expected_result in result)

        self.driver.find_element_by_css_selector(".form-control[name='last_name']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='last_name']").send_keys('v')
        self.driver.find_element_by_tag_name('button').click()

        self.assertEqual(len(result), 2)

        expected_result = ['volunteer-first-nameq', 'volunteer-last-name',
                'volunteer-addressq', 'volunteer-cityq', 'volunteer-stateq',
                'volunteer-countryq', 'volunteer-organizationq', '9999999999',
                'volunteer-email@systers.orgq']
        
        self.assertTrue(expected_result in result)

        expected_result = ['volunteer-first-name', 'VOLUNTEER-LAST-NAME',
                'volunteer-address', 'volunteer-city', 'volunteer-state',
                'volunteer-country', 'volunteer-organization', '9999999999',
                'volunteer-email@systers.org']

        self.assertTrue(expected_result in result)

        self.driver.find_element_by_css_selector(".form-control[name='last_name']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='last_name']").send_keys('vol-')
        self.driver.find_element_by_tag_name('button').click()

        with self.assertRaises(NoSuchElementException):
            search_results = self.driver.find_element_by_xpath('//table//tbody')

        self.driver.find_element_by_css_selector(".form-control[name='last_name']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='last_name']").send_keys('volunteer-fail-test')
        self.driver.find_element_by_tag_name('button').click()

        with self.assertRaises(NoSuchElementException):
            search_results = self.driver.find_element_by_xpath('//table//tbody')

        self.driver.find_element_by_css_selector(".form-control[name='last_name']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='last_name']").send_keys('!@#$%^&*()_')
        self.driver.find_element_by_tag_name('button').click()
        self.assertNotEqual(self.driver.find_element_by_class_name('help-block'),
                None)

    def test_volunteer_city_field(self):            
        credentials = ['volunteer-username', 'volunteer-password',
                'volunteer-first-name', 'volunteer-last-name',
                'volunteer-email@systers.org', 'volunteer-address',
                'VOLUNTEER-CITY', 'volunteer-state', 'volunteer-country',
                '9999999999', 'volunteer-organization']

        self.register_volunteer(credentials)

        credentials = ['volunteer-usernameq', 'volunteer-passwordq',
                'volunteer-first-nameq', 'volunteer-last-nameq',
                'volunteer-email@systers.orgq', 'volunteer-addressq',
                'volunteer-city', 'volunteer-stateq', 'volunteer-countryq',
                '9999999999', 'volunteer-organizationq']

        self.register_volunteer(credentials)

        self.login_admin()
        self.driver.get(self.live_server_url + '/volunteer/search/')
        self.assertEqual(self.driver.current_url, self.live_server_url +
                '/volunteer/search/')

        self.driver.find_element_by_css_selector(".form-control[name='city']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='city']").send_keys('volunteer')
        self.driver.find_element_by_tag_name('button').click()

        search_results = self.driver.find_element_by_xpath('//table//tbody')

        result = []
        for tr in search_results.find_elements_by_tag_name('tr'):
            row = tr.text.split()
            result.append(row)

        expected_result = ['volunteer-first-nameq', 'volunteer-last-nameq',
                'volunteer-addressq', 'volunteer-city', 'volunteer-stateq',
                'volunteer-countryq', 'volunteer-organizationq', '9999999999',
                'volunteer-email@systers.orgq']
        
        self.assertTrue(expected_result in result)

        expected_result = ['volunteer-first-name', 'volunteer-last-name',
                'volunteer-address', 'VOLUNTEER-CITY', 'volunteer-state',
                'volunteer-country', 'volunteer-organization', '9999999999',
                'volunteer-email@systers.org']

        self.assertTrue(expected_result in result)

        self.driver.find_element_by_css_selector(".form-control[name='city']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='city']").send_keys('v')
        self.driver.find_element_by_tag_name('button').click()

        self.assertEqual(len(result), 2)

        expected_result = ['volunteer-first-nameq', 'volunteer-last-nameq',
                'volunteer-addressq', 'volunteer-city', 'volunteer-stateq',
                'volunteer-countryq', 'volunteer-organizationq', '9999999999',
                'volunteer-email@systers.orgq']
        
        self.assertTrue(expected_result in result)

        expected_result = ['volunteer-first-name', 'volunteer-last-name',
                'volunteer-address', 'VOLUNTEER-CITY', 'volunteer-state',
                'volunteer-country', 'volunteer-organization', '9999999999',
                'volunteer-email@systers.org']

        self.assertTrue(expected_result in result)

        self.driver.find_element_by_css_selector(".form-control[name='city']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='city']").send_keys('vol-')
        self.driver.find_element_by_tag_name('button').click()

        with self.assertRaises(NoSuchElementException):
            search_results = self.driver.find_element_by_xpath('//table//tbody')

        self.driver.find_element_by_css_selector(".form-control[name='city']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='city']").send_keys('volunteer-fail-test')
        self.driver.find_element_by_tag_name('button').click()

        with self.assertRaises(NoSuchElementException):
            search_results = self.driver.find_element_by_xpath('//table//tbody')

        self.driver.find_element_by_css_selector(".form-control[name='city']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='city']").send_keys('!@#$%^&*()_')
        self.driver.find_element_by_tag_name('button').click()
        self.assertNotEqual(self.driver.find_element_by_class_name('help-block'),
                None)

    def test_volunteer_state_field(self):            
        credentials = ['volunteer-username', 'volunteer-password',
                'volunteer-first-name', 'volunteer-last-name',
                'volunteer-email@systers.org', 'volunteer-address',
                'volunteer-city', 'VOLUNTEER-STATE', 'volunteer-country',
                '9999999999', 'volunteer-organization']

        self.register_volunteer(credentials)

        credentials = ['volunteer-usernameq', 'volunteer-passwordq',
                'volunteer-first-nameq', 'volunteer-last-nameq',
                'volunteer-email@systers.orgq', 'volunteer-addressq',
                'volunteer-cityq', 'volunteer-state', 'volunteer-countryq',
                '9999999999', 'volunteer-organizationq']

        self.register_volunteer(credentials)

        self.login_admin()
        self.driver.get(self.live_server_url + '/volunteer/search/')
        self.assertEqual(self.driver.current_url, self.live_server_url +
                '/volunteer/search/')

        self.driver.find_element_by_css_selector(".form-control[name='state']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='state']").send_keys('volunteer')
        self.driver.find_element_by_tag_name('button').click()

        search_results = self.driver.find_element_by_xpath('//table//tbody')

        result = []
        for tr in search_results.find_elements_by_tag_name('tr'):
            row = tr.text.split()
            result.append(row)

        expected_result = ['volunteer-first-nameq', 'volunteer-last-nameq',
                'volunteer-addressq', 'volunteer-cityq', 'volunteer-state',
                'volunteer-countryq', 'volunteer-organizationq', '9999999999',
                'volunteer-email@systers.orgq']
        
        self.assertTrue(expected_result in result)

        expected_result = ['volunteer-first-name', 'volunteer-last-name',
                'volunteer-address', 'volunteer-city', 'VOLUNTEER-STATE',
                'volunteer-country', 'volunteer-organization', '9999999999',
                'volunteer-email@systers.org']

        self.assertTrue(expected_result in result)

        self.driver.find_element_by_css_selector(".form-control[name='state']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='state']").send_keys('v')
        self.driver.find_element_by_tag_name('button').click()

        self.assertEqual(len(result), 2)

        expected_result = ['volunteer-first-nameq', 'volunteer-last-nameq',
                'volunteer-addressq', 'volunteer-cityq', 'volunteer-state',
                'volunteer-countryq', 'volunteer-organizationq', '9999999999',
                'volunteer-email@systers.orgq']
        
        self.assertTrue(expected_result in result)

        expected_result = ['volunteer-first-name', 'volunteer-last-name',
                'volunteer-address', 'volunteer-city', 'VOLUNTEER-STATE',
                'volunteer-country', 'volunteer-organization', '9999999999',
                'volunteer-email@systers.org']

        self.assertTrue(expected_result in result)

        self.driver.find_element_by_css_selector(".form-control[name='state']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='state']").send_keys('vol-')
        self.driver.find_element_by_tag_name('button').click()

        with self.assertRaises(NoSuchElementException):
            search_results = self.driver.find_element_by_xpath('//table//tbody')

        self.driver.find_element_by_css_selector(".form-control[name='state']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='state']").send_keys('volunteer-fail-test')
        self.driver.find_element_by_tag_name('button').click()

        with self.assertRaises(NoSuchElementException):
            search_results = self.driver.find_element_by_xpath('//table//tbody')

        self.driver.find_element_by_css_selector(".form-control[name='state']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='state']").send_keys('!@#$%^&*()_')
        self.driver.find_element_by_tag_name('button').click()
        self.assertNotEqual(self.driver.find_element_by_class_name('help-block'),
                None)

    def test_volunteer_country_field(self):            
        credentials = ['volunteer-username', 'volunteer-password',
                'volunteer-first-name', 'volunteer-last-name',
                'volunteer-email@systers.org', 'volunteer-address',
                'volunteer-city', 'volunteer-state', 'VOLUNTEER-COUNTRY',
                '9999999999', 'volunteer-organization']

        self.register_volunteer(credentials)

        credentials = ['volunteer-usernameq', 'volunteer-passwordq',
                'volunteer-first-nameq', 'volunteer-last-nameq',
                'volunteer-email@systers.orgq', 'volunteer-addressq',
                'volunteer-cityq', 'volunteer-stateq', 'volunteer-country',
                '9999999999', 'volunteer-organizationq']

        self.register_volunteer(credentials)

        self.login_admin()
        self.driver.get(self.live_server_url + '/volunteer/search/')
        self.assertEqual(self.driver.current_url, self.live_server_url +
                '/volunteer/search/')

        self.driver.find_element_by_css_selector(".form-control[name='country']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='country']").send_keys('volunteer')
        self.driver.find_element_by_tag_name('button').click()

        search_results = self.driver.find_element_by_xpath('//table//tbody')

        result = []
        for tr in search_results.find_elements_by_tag_name('tr'):
            row = tr.text.split()
            result.append(row)

        expected_result = ['volunteer-first-nameq', 'volunteer-last-nameq',
                'volunteer-addressq', 'volunteer-cityq', 'volunteer-stateq',
                'volunteer-country', 'volunteer-organizationq', '9999999999',
                'volunteer-email@systers.orgq']
        
        self.assertTrue(expected_result in result)

        expected_result = ['volunteer-first-name', 'volunteer-last-name',
                'volunteer-address', 'volunteer-city', 'volunteer-state',
                'VOLUNTEER-COUNTRY', 'volunteer-organization', '9999999999',
                'volunteer-email@systers.org']

        self.assertTrue(expected_result in result)

        self.driver.find_element_by_css_selector(".form-control[name='country']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='country']").send_keys('v')
        self.driver.find_element_by_tag_name('button').click()

        self.assertEqual(len(result), 2)

        expected_result = ['volunteer-first-nameq', 'volunteer-last-nameq',
                'volunteer-addressq', 'volunteer-cityq', 'volunteer-stateq',
                'volunteer-country', 'volunteer-organizationq', '9999999999',
                'volunteer-email@systers.orgq']
        
        self.assertTrue(expected_result in result)

        expected_result = ['volunteer-first-name', 'volunteer-last-name',
                'volunteer-address', 'volunteer-city', 'volunteer-state',
                'VOLUNTEER-COUNTRY', 'volunteer-organization', '9999999999',
                'volunteer-email@systers.org']

        self.assertTrue(expected_result in result)

        self.driver.find_element_by_css_selector(".form-control[name='country']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='country']").send_keys('vol-')
        self.driver.find_element_by_tag_name('button').click()

        with self.assertRaises(NoSuchElementException):
            search_results = self.driver.find_element_by_xpath('//table//tbody')

        self.driver.find_element_by_css_selector(".form-control[name='country']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='country']").send_keys('volunteer-fail-test')
        self.driver.find_element_by_tag_name('button').click()

        with self.assertRaises(NoSuchElementException):
            search_results = self.driver.find_element_by_xpath('//table//tbody')

        self.driver.find_element_by_css_selector(".form-control[name='country']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='country']").send_keys('!@#$%^&*()_')
        self.driver.find_element_by_tag_name('button').click()
        self.assertNotEqual(self.driver.find_element_by_class_name('help-block'),
                None)

    def test_volunteer_organization_field(self):            
        credentials = ['volunteer-username', 'volunteer-password',
                'volunteer-first-name', 'volunteer-last-name',
                'volunteer-email@systers.org', 'volunteer-address',
                'volunteer-city', 'volunteer-state', 'volunteer-country',
                '9999999999', 'VOLUNTEER-ORGANIZATION']

        self.register_volunteer(credentials)

        credentials = ['volunteer-usernameq', 'volunteer-passwordq',
                'volunteer-first-nameq', 'volunteer-last-nameq',
                'volunteer-email@systers.orgq', 'volunteer-addressq',
                'volunteer-cityq', 'volunteer-stateq', 'volunteer-countryq',
                '9999999999', 'volunteer-organization']

        self.register_volunteer(credentials)

        self.login_admin()
        self.driver.get(self.live_server_url + '/volunteer/search/')
        self.assertEqual(self.driver.current_url, self.live_server_url +
                '/volunteer/search/')

        self.driver.find_element_by_css_selector(".form-control[name='organization']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='organization']").send_keys('volunteer')
        self.driver.find_element_by_tag_name('button').click()

        search_results = self.driver.find_element_by_xpath('//table//tbody')

        result = []
        for tr in search_results.find_elements_by_tag_name('tr'):
            row = tr.text.split()
            result.append(row)

        expected_result = ['volunteer-first-nameq', 'volunteer-last-nameq',
                'volunteer-addressq', 'volunteer-cityq', 'volunteer-stateq',
                'volunteer-countryq', 'volunteer-organization', '9999999999',
                'volunteer-email@systers.orgq']
        
        self.assertTrue(expected_result in result)

        expected_result = ['volunteer-first-name', 'volunteer-last-name',
                'volunteer-address', 'volunteer-city', 'volunteer-state',
                'volunteer-country', 'VOLUNTEER-ORGANIZATION', '9999999999',
                'volunteer-email@systers.org']

        self.assertTrue(expected_result in result)

        self.driver.find_element_by_css_selector(".form-control[name='organization']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='organization']").send_keys('v')
        self.driver.find_element_by_tag_name('button').click()

        self.assertEqual(len(result), 2)

        expected_result = ['volunteer-first-nameq', 'volunteer-last-nameq',
                'volunteer-addressq', 'volunteer-cityq', 'volunteer-stateq',
                'volunteer-countryq', 'volunteer-organization', '9999999999',
                'volunteer-email@systers.orgq']
        
        self.assertTrue(expected_result in result)

        expected_result = ['volunteer-first-name', 'volunteer-last-name',
                'volunteer-address', 'volunteer-city', 'volunteer-state',
                'volunteer-country', 'VOLUNTEER-ORGANIZATION', '9999999999',
                'volunteer-email@systers.org']

        self.assertTrue(expected_result in result)

        self.driver.find_element_by_css_selector(".form-control[name='organization']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='organization']").send_keys('vol-')
        self.driver.find_element_by_tag_name('button').click()

        with self.assertRaises(NoSuchElementException):
            search_results = self.driver.find_element_by_xpath('//table//tbody')

        self.driver.find_element_by_css_selector(".form-control[name='organization']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='organization']").send_keys('volunteer-fail-test')
        self.driver.find_element_by_tag_name('button').click()

        with self.assertRaises(NoSuchElementException):
            search_results = self.driver.find_element_by_xpath('//table//tbody')

        self.driver.find_element_by_css_selector(".form-control[name='organization']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='organization']").send_keys('!@#$%^&*()_')
        self.driver.find_element_by_tag_name('button').click()
        self.assertNotEqual(self.driver.find_element_by_class_name('help-block'),
                None)

    def test_intersection_of_all_fields(self):            
        credentials = ['volunteer-username', 'volunteer-password',
                'volunteer-first-name', 'volunteer-last-name',
                'volunteer-email@systers.org', 'volunteer-address',
                'volunteer-city', 'volunteer-state', 'volunteer-country',
                '9999999999', 'VOLUNTEER-ORGANIZATION']

        self.register_volunteer(credentials)

        credentials = ['volunteer-usernameq', 'volunteer-passwordq',
                'volunteer-first-nameq', 'volunteer-last-nameq',
                'volunteer-email@systers.orgq', 'volunteer-addressq',
                'volunteer-cityq', 'volunteer-stateq', 'volunteer-countryq',
                '9999999999', 'volunteer-organization']

        self.register_volunteer(credentials)

        self.login_admin()
        self.driver.get(self.live_server_url + '/volunteer/search/')
        self.assertEqual(self.driver.current_url, self.live_server_url +
                '/volunteer/search/')

        self.driver.find_element_by_css_selector(".form-control[name='first_name']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='first_name']").send_keys('volunteer')
        self.driver.find_element_by_css_selector(".form-control[name='last_name']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='last_name']").send_keys('volunteer')
        self.driver.find_element_by_css_selector(".form-control[name='city']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='city']").send_keys('volunteer')
        self.driver.find_element_by_css_selector(".form-control[name='state']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='state']").send_keys('volunteer')
        self.driver.find_element_by_css_selector(".form-control[name='country']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='country']").send_keys('volunteer')
        self.driver.find_element_by_css_selector(".form-control[name='organization']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='organization']").send_keys('volunteer')
        self.driver.find_element_by_tag_name('button').click()

        search_results = self.driver.find_element_by_xpath('//table//tbody')

        result = []
        for tr in search_results.find_elements_by_tag_name('tr'):
            row = tr.text.split()
            result.append(row)

        expected_result = ['volunteer-first-nameq', 'volunteer-last-nameq',
                'volunteer-addressq', 'volunteer-cityq', 'volunteer-stateq',
                'volunteer-countryq', 'volunteer-organization', '9999999999',
                'volunteer-email@systers.orgq']
        
        self.assertTrue(expected_result in result)

        expected_result = ['volunteer-first-name', 'volunteer-last-name',
                'volunteer-address', 'volunteer-city', 'volunteer-state',
                'volunteer-country', 'VOLUNTEER-ORGANIZATION', '9999999999',
                'volunteer-email@systers.org']

        self.assertTrue(expected_result in result)

        self.driver.find_element_by_css_selector(".form-control[name='first_name']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='first_name']").send_keys('volunteer')
        self.driver.find_element_by_css_selector(".form-control[name='country']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='country']").send_keys('wrong-country')
        self.driver.find_element_by_css_selector(".form-control[name='organization']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='organization']").send_keys('org')
        self.driver.find_element_by_tag_name('button').click()

        with self.assertRaises(NoSuchElementException):
            search_results = self.driver.find_element_by_xpath('//table//tbody')
        
        self.driver.find_element_by_css_selector(".form-control[name='last_name']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='last_name']").send_keys('volunteer')
        self.driver.find_element_by_css_selector(".form-control[name='city']").clear()
        self.driver.find_element_by_css_selector(".form-control[name='city']").send_keys('wrong-city')
        self.driver.find_element_by_tag_name('button').click()

        with self.assertRaises(NoSuchElementException):
            search_results = self.driver.find_element_by_xpath('//table//tbody')
