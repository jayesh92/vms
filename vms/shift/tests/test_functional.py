from django.test import TestCase
from django.contrib.staticfiles.testing import LiveServerTestCase

from django.contrib.auth.models import User
from administrator.models import Administrator

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class ManageVolunteerShift(LiveServerTestCase):
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
        self.shift_page = '/shift/volunteer_search/'
        self.volunteer_registration_page = '/registration/signup_volunteer/'
        self.settings_page = '/event/list/'
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        super(ManageVolunteerShift, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(ManageVolunteerShift, self).tearDown()

    def login_admin(self):
        self.driver.get(self.live_server_url + self.authentication_page)
        self.driver.find_element_by_id('id_login').send_keys('admin')
        self.driver.find_element_by_id('id_password').send_keys('admin')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertEqual(self.driver.current_url,
                self.live_server_url + self.homepage)

    def register_volunteer(self, credentials):
        self.driver.get(self.live_server_url
                        + self.volunteer_registration_page)

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

        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name('help-block'),

        self.assertEqual(self.driver.current_url,
                self.live_server_url + self.homepage)

    def register_test_dataset(self):
        credentials = ['volunteer-one', 'volunteer-password',
                'volunteer-one', 'volunteer-one', 'volunteer-email@systers.org',
                'volunteer-one', 'volunteer-one', 'volunteer-one',
                'volunteer-one', '9999999999', 'volunteer-one']

        self.register_volunteer(credentials)

        credentials = ['volunteer-two', 'volunteer-password',
                'volunteer-two', 'volunteer-two', 'volunteer-email@systers.org',
                'volunteer-two', 'volunteer-two', 'volunteer-two',
                'volunteer-two', '9999999999', 'volunteer-two']

        self.register_volunteer(credentials)

    def test_page1_without_any_registered_volunteers(self):
        self.login_admin()
        self.driver.find_element_by_link_text('Manage Volunteer Shifts').click()
        self.assertEqual(self.driver.current_url,
                self.live_server_url + self.shift_page)
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_tag_name('tr')

    def test_page1_with_registered_volunteers(self):
        # register volunteers
        self.register_test_dataset()

        # login admin user
        self.login_admin()

        # open manage volunteer shift
        self.driver.find_element_by_link_text('Manage Volunteer Shifts').click()
        self.assertEqual(self.driver.current_url,
                self.live_server_url + self.shift_page)

        self.assertNotEqual(self.driver.find_element_by_tag_name('tr'), None)

        self.driver.find_element_by_xpath('//table//tbody//tr[1]//td[10]//a').click()
        self.assertEqual(self.driver.find_element_by_class_name('alert-info').text,
               'This volunteer does not have any upcoming shifts.')

        self.driver.back()
        self.assertEqual(self.driver.current_url, 
                self.live_server_url + '/shift/volunteer_search/')

        self.driver.find_element_by_xpath('//table//tbody//tr[2]//td[10]//a').click()
        self.assertEqual(self.driver.find_element_by_class_name('alert-info').text,
               'This volunteer does not have any upcoming shifts.')

    def test_page2_with_no_events(self):
        # register volunteers
        self.register_test_dataset()

        # login admin user
        self.login_admin()

        # open manage volunteer shift
        self.driver.find_element_by_link_text('Manage Volunteer Shifts').click()
        self.assertEqual(self.driver.current_url,
                self.live_server_url + self.shift_page)

        self.driver.find_element_by_xpath('//table//tbody//tr[1]//td[10]//a').click()

        self.driver.find_element_by_link_text('Assign Shift').click()

        self.assertEqual(self.driver.find_element_by_class_name('alert-info').text,
               'There are currently no events.')

    def register_event_utility(self, event):
        self.driver.find_element_by_link_text('Settings').click()
        self.assertEqual(self.driver.current_url,
                self.live_server_url +  self.settings_page)

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

        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name('help-block'),

    def test_page2_with_registered_events(self):
        # register volunteers
        self.register_test_dataset()

        # login admin
        self.login_admin()

        # create events
        event = ['event-name', '05/20/2015', '05/20/2015']
        self.register_event_utility(event)

        # open manage volunteer shift
        self.driver.find_element_by_link_text(
                'Manage Volunteer Shifts').click()
        self.assertEqual(self.driver.current_url,
                self.live_server_url +  self.shift_page)

        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[10]//a').click()

        self.driver.find_element_by_link_text('Assign Shift').click()

        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name('alert-info')

        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[4]//a').click()

        # arrived on jobs page with no jobs
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_tag_name('table')
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-info').text, 'There are currently no jobs for event-name.')

    def register_job_utility(self, job):
        self.assertEqual(self.driver.current_url,
                self.live_server_url +  self.settings_page)
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

        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name('help-block'),

    def test_page2_with_registered_jobs(self):
        # register volunteers
        self.register_test_dataset()

        # login admin
        self.login_admin()

        # create events
        event = ['event-name', '05/20/2015', '05/20/2015']
        self.register_event_utility(event)

        # create jobs
        job = ['event-name', 'job name', 'job description', '05/20/2015',
            '05/20/2015']
        self.register_job_utility(job)

        # open manage volunteer shift
        self.driver.find_element_by_link_text(
                'Manage Volunteer Shifts').click()
        self.assertEqual(self.driver.current_url,
                self.live_server_url +  self.shift_page)

        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[10]//a').click()

        self.driver.find_element_by_link_text('Assign Shift').click()

        # events shown in table
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name('alert-info')

        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[4]//a').click()

        # arrived on page2 with jobs
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text,
            'job name')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[4]//a').click()

        # arrived on page3 with no shifts in job created
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-info').text,
            'There are currently no shifts for the job name job.')

    def register_shift_utility(self, shift):
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
                        shift[0])
        self.driver.find_element_by_xpath(
                '//input[@name = "start_time"]').send_keys(
                        shift[1])
        self.driver.find_element_by_xpath(
                '//input[@name = "end_time"]').send_keys(
                        shift[2])
        self.driver.find_element_by_xpath(
                '//input[@name = "max_volunteers"]').send_keys(
                        shift[3])
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertNotEqual(self.driver.find_elements_by_xpath(
                '//table//tbody'), None)

    def test_page3_with_registered_shifts(self):
        # register volunteers
        self.register_test_dataset()

        # create shift to assign
        shift = ['06/20/2015', '09:00', '15:00', '1']
        self.register_shift_utility(shift)

        # open manage volunteer shift
        self.driver.find_element_by_link_text(
                'Manage Volunteer Shifts').click()
        self.assertEqual(self.driver.current_url,
                self.live_server_url +  self.shift_page)

        # volunteer-one does not have any registered shifts
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[10]').text,
            'Manage Shifts')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[10]//a').click()
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-info').text, 
            'This volunteer does not have any upcoming shifts.')

        self.driver.find_element_by_link_text('Assign Shift').click()

        # events shown in table
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name('alert-info')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[4]').text,
            'View Jobs')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[4]//a').click()

        # arrived on page2 with jobs
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[4]').text,
            'View Shifts')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[4]//a').click()

        # arrived on page3 with shifts, assign shift to volunteer one
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[4]').text,
            'Assign Shift')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[4]//a').click()

        # confirm on shift assignment to volunteer-one
        self.driver.find_element_by_xpath('//form[1]').submit()
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name('alert-danger')

        # check shift assignment to volunteer-one
        self.driver.find_element_by_link_text(
                'Manage Volunteer Shifts').click()
        self.assertEqual(self.driver.current_url,
                self.live_server_url +  self.shift_page)
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[10]').text,
            'Manage Shifts')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[10]//a').click()
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text,
            'job name')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[2]').text,
            'June 20, 2015')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[3]').text,
            '9 a.m.')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[4]').text,
            '3 p.m.')
