from django.test import TestCase
from django.contrib.staticfiles.testing import LiveServerTestCase

from django.contrib.auth.models import User
from administrator.models import Administrator

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class Settings(LiveServerTestCase):
    '''
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

        self.homepage = '/home/'
        self.authentication_page = '/authentication/login/'
        self.settings_page = '/event/list/'
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        super(Settings, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(Settings, self).tearDown()

    def login_admin(self):
        self.driver.get(self.live_server_url + self.authentication_page)
        self.driver.find_element_by_id('id_login').send_keys('admin')
        self.driver.find_element_by_id('id_password').send_keys('admin')
        self.driver.find_element_by_xpath('//form[1]').submit()
        self.driver.find_element_by_link_text('Settings').click()

        self.assertEqual(self.driver.current_url,
                self.live_server_url + self.settings_page)

    def test_event_tab(self):
        self.login_admin()
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-success').text,
            'There are currently no events. Please create events first.')

    def test_job_tab(self):
        self.login_admin()
        self.driver.find_element_by_link_text('Jobs').click()
        self.assertEqual(self.driver.current_url,
                self.live_server_url + '/job/list/')
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-success').text,
            'There are currently no jobs. Please create jobs first.')

        self.driver.find_element_by_link_text('Create Job').click()
        self.assertEqual(self.driver.current_url,
                self.live_server_url + '/job/create/')
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-success').text,
            'Please add events to associate with jobs first.')

    def test_shift_tab(self):
        self.login_admin()
        self.driver.find_element_by_link_text('Shifts').click()
        self.assertEqual(self.driver.current_url,
                self.live_server_url + '/shift/list_jobs/')
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-success').text,
            'There are currently no jobs. Please create jobs first.')

    def register_event_utility(self, event):
        self.driver.find_element_by_link_text('Create Event').click()
        self.assertEqual(self.driver.current_url,
                self.live_server_url + '/event/create/')

        self.driver.find_element_by_xpath(
                '//input[@placeholder = "Event Name"]').send_keys(
                        event[0])
        self.driver.find_element_by_xpath(
                '//input[@name = "start_date"]').send_keys(
                        event[1])
        self.driver.find_element_by_xpath(
                '//input[@name = "end_date"]').send_keys(
                        event[2])
        self.driver.find_element_by_xpath('//form[1]').submit()

    def register_job_utility(self, job):
        self.driver.find_element_by_link_text('Jobs').click()
        self.assertEqual(self.driver.current_url,
                self.live_server_url + '/job/list/')

        self.driver.find_element_by_link_text('Create Job').click()
        self.assertEqual(self.driver.current_url,
                self.live_server_url + '/job/create/')

        self.driver.find_element_by_xpath(
                '//select[@name = "event_id"]').send_keys(
                        job[0])
        self.driver.find_element_by_xpath(
                '//input[@placeholder = "Job Name"]').send_keys(
                        job[1])
        self.driver.find_element_by_xpath(
                '//textarea[@name = "description"]').send_keys(
                        job[2])
        self.driver.find_element_by_xpath(
                '//input[@name = "start_date"]').send_keys(
                        job[3])
        self.driver.find_element_by_xpath(
                '//input[@name = "end_date"]').send_keys(
                        job[4])
        self.driver.find_element_by_xpath('//form[1]').submit()

    def test_create_event(self):
        self.login_admin()
        event = ['event-name', '05/20/2015', '05/20/2015']
        self.register_event_utility(event)
        
        # check event created
        self.assertEqual(self.driver.current_url,
                self.live_server_url + self.settings_page)
        self.assertEqual(self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[1]').text, 'event-name')

    def test_create_job(self):
        self.login_admin()

        # register event first to create job
        event = ['event-name', '05/20/2015', '05/20/2015']
        self.register_event_utility(event)

        # create job
        job = ['event-name', 'job name', 'job description', '05/20/2015', 
                '05/20/2015']
        self.assertEqual(self.driver.current_url,
                self.live_server_url + self.settings_page)
        self.register_job_utility(job)

        # check job created
        self.assertEqual(self.driver.current_url,
                self.live_server_url + '/job/list/')
        self.assertEqual(self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[1]').text, 'job name')
        self.assertEqual(self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[2]').text, 'event-name')

    def test_create_shift(self):
        self.login_admin()

        # register event to create job
        event = ['event-name', '05/20/2015', '05/20/2015']
        self.register_event_utility(event)

        # create job to create shift
        job = ['event-name', 'job name', 'job description', '05/20/2015', 
                '05/20/2015']
        self.register_job_utility(job)

        # create shift
        self.driver.find_element_by_link_text('Shifts').click()
        self.assertEqual(self.driver.current_url,
                self.live_server_url + '/shift/list_jobs/')

        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]/td[5]//a').click()

        self.driver.find_element_by_link_text('Create Shift').click()

        self.driver.find_element_by_xpath(
                '//input[@name = "date"]').send_keys(
                        '06/20/2015')
        self.driver.find_element_by_xpath(
                '//input[@name = "start_time"]').send_keys(
                        '09:00')
        self.driver.find_element_by_xpath(
                '//input[@name = "end_time"]').send_keys(
                        '12:00')
        self.driver.find_element_by_xpath(
                '//input[@name = "max_volunteers"]').send_keys(
                        '10')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertNotEqual(self.driver.find_elements_by_xpath(
                '//table//tbody'), None)
