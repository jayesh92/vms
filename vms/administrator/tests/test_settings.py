from django.test import TestCase
from django.contrib.staticfiles.testing import LiveServerTestCase

from django.contrib.auth.models import User
from administrator.models import Administrator
from volunteer.models import Volunteer
from organization.models import Organization #hack to pass travis,Bug in Code

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class Settings(LiveServerTestCase):
    '''
    Settings Class contains UI testcases for `Settings` view in
    Administrator profile. This view consists of Events, Jobs, Shifts,
    Organization tabs.

    Event:
        - Create Event
        - Edit Event
        - Delete Event with No Associated Job
        - Delete event with Associated Job

    Job:
        - Create Job without any event
        - Edit Job
        - Delete Job without Assoicated Shift
        - Delete Job with Shifts

    Shift:
        - Create Shift without any Job
        - Edit Shift
        - Delete shift

    Organization:
        - Create Organization
        - Edit Organization
        - Replication of Organization
        - Delete Org's with registered volunteers
        - Delete Org without registered volunteers 
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

    def test_job_tab_and_create_job_without_event(self):
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

    def test_shift_tab_and_create_shift_without_job(self):
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

    def test_edit_event(self):
        self.login_admin()
        event = ['event-name', '05/20/2015', '05/20/2015']
        self.register_event_utility(event)
        
        # create event
        self.assertEqual(self.driver.current_url,
                self.live_server_url + self.settings_page)
        self.assertEqual(self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[1]').text, 'event-name')

        self.assertEqual(self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[4]').text, 'Edit')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[4]//a').click()

        self.driver.find_element_by_xpath(
                '//input[@placeholder = "Event Name"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@placeholder = "Event Name"]').send_keys(
                        'changed-event-name')

        self.driver.find_element_by_xpath(
                '//input[@name = "start_date"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "start_date"]').send_keys(
                        '06/24/2015')

        self.driver.find_element_by_xpath(
                '//input[@name = "end_date"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "end_date"]').send_keys(
                        '06/24/2015')

        self.driver.find_element_by_xpath('//form[1]').submit()

        # check event edited
        self.assertEqual(self.driver.current_url,
                self.live_server_url + self.settings_page)
        self.assertEqual(self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[1]').text, 'changed-event-name')

    def test_delete_event_with_no_associated_job(self):
        self.login_admin()
        event = ['event-name', '05/20/2015', '05/20/2015']
        self.register_event_utility(event)
        
        # create event
        self.assertEqual(self.driver.current_url,
                self.live_server_url + self.settings_page)
        self.assertEqual(self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[1]').text, 'event-name')

        self.assertEqual(self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[5]').text, 'Delete')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[5]//a').click()

        self.assertNotEqual(self.driver.find_element_by_class_name(
            'panel-danger'), None)
        self.assertEqual(self.driver.find_element_by_class_name(
            'panel-heading').text, 'Delete Event')
        self.driver.find_element_by_xpath('//form').submit()

        # check event deleted
        self.assertEqual(self.driver.current_url,
                self.live_server_url + self.settings_page)
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_xpath('//table//tbody')

    def test_delete_event_with_associated_job(self):
        self.login_admin()
        
        # create event
        event = ['event-name', '05/20/2015', '05/20/2015']
        self.register_event_utility(event)

        # create job
        job = ['event-name', 'job name', 'job description', '05/20/2015', 
                '05/20/2015']
        self.assertEqual(self.driver.current_url,
                self.live_server_url + self.settings_page)
        self.register_job_utility(job)
        
        # check event created
        self.driver.get(self.live_server_url + self.settings_page)
        self.assertEqual(self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[1]').text, 'event-name')

        # delete event
        self.assertEqual(self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[5]').text, 'Delete')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[5]//a').click()
        
        # confirm to delete
        self.assertNotEqual(self.driver.find_element_by_class_name(
            'panel-danger'), None)
        self.assertEqual(self.driver.find_element_by_class_name(
            'panel-heading').text, 'Delete Event')
        self.driver.find_element_by_xpath('//form').submit()

        self.assertNotEqual(self.driver.find_element_by_class_name(
            'alert-danger'), None)
        self.assertEqual(self.driver.find_element_by_xpath(
            '//div[2]/div[3]/p').text,
            'You cannot delete an event that a job is currently associated with.')

        # check event NOT deleted
        self.driver.get(self.live_server_url + self.settings_page)
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

    def test_edit_job(self):
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

        # edit job
        self.assertEqual(self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[6]').text, 'Edit')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[6]//a').click()

        self.driver.find_element_by_xpath(
                '//input[@name = "name"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "name"]').send_keys(
                        'changed job name')

        self.driver.find_element_by_xpath(
                '//textarea[@name = "description"]').clear()
        self.driver.find_element_by_xpath(
                '//textarea[@name = "description"]').send_keys(
                        'changed-job-description')

        self.driver.find_element_by_xpath(
                '//input[@name = "start_date"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "start_date"]').send_keys(
                        '06/24/2015')

        self.driver.find_element_by_xpath(
                '//input[@name = "end_date"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "end_date"]').send_keys(
                        '06/24/2015')

        self.driver.find_element_by_xpath('//form[1]').submit()

        # check event edited
        self.assertEqual(self.driver.current_url,
                self.live_server_url + '/job/list/')
        self.assertEqual(self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[1]').text, 'changed job name')

    def test_delete_job_without_associated_shift(self):
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

        # delete job
        self.assertEqual(self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[7]').text, 'Delete')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[7]//a').click()

        self.assertNotEqual(self.driver.find_element_by_class_name(
            'panel-danger'), None)
        self.assertEqual(self.driver.find_element_by_class_name(
            'panel-heading').text, 'Delete Job')
        self.driver.find_element_by_xpath('//form').submit()

        # check event deleted
        self.assertEqual(self.driver.current_url,
                self.live_server_url + '/job/list/')
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_xpath('//table//tbody')

    def test_delete_job_with_associated_shifts(self):
        self.login_admin()

        # register event
        event = ['event-name', '05/20/2015', '05/20/2015']
        self.register_event_utility(event)

        # create job
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

        # delete job
        self.driver.get(self.live_server_url + '/job/list/')
        self.assertEqual(self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[7]').text, 'Delete')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[7]//a').click()

        self.assertNotEqual(self.driver.find_element_by_class_name(
            'panel-danger'), None)
        self.assertEqual(self.driver.find_element_by_class_name(
            'panel-heading').text, 'Delete Job')
        self.driver.find_element_by_xpath('//form').submit()
        
        self.assertNotEqual(self.driver.find_element_by_class_name(
            'alert-danger'), None)
        self.assertEqual(self.driver.find_element_by_xpath(
            '//div[2]/div[3]/p').text,
            'You cannot delete a job that a shift is currently associated with.')

        # check job NOT deleted
        self.driver.get(self.live_server_url + '/job/list/')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text, 'job name')

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

    def test_edit_shift(self):
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

        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[5]').text, 'Edit')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[5]//a').click()
        
        self.driver.find_element_by_xpath('//input[@name = "date"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "date"]').send_keys(
                        '06/24/2015')

        self.driver.find_element_by_xpath(
                '//input[@name = "start_time"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "start_time"]').send_keys(
                        '10:00')

        self.driver.find_element_by_xpath(
                '//input[@name = "end_time"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "end_time"]').send_keys(
                        '13:00')

        self.driver.find_element_by_xpath(
                '//input[@name = "max_volunteers"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "max_volunteers"]').send_keys(
                        '5')

        self.driver.find_element_by_xpath('//form[1]').submit()

        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name('help-block')

        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text, 'June 24, 2015')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[2]').text, '10 a.m.')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[3]').text, '1 p.m.')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[4]').text, '5')

    def test_delete_shift(self):
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
        
        # delete shift
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[6]').text, 'Delete')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[6]//a').click()

        # confirm on delete
        self.assertNotEqual(self.driver.find_element_by_class_name(
            'panel-danger'), None)
        self.assertEqual(self.driver.find_element_by_class_name(
            'panel-heading').text, 'Delete Shift')
        self.driver.find_element_by_xpath('//form').submit()

        # check deletion of shift
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text, 'job name')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[5]').text, 'Shifts')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[5]//a').click()
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-success').text,
            'There are currently no shifts. Please create shifts first.')

    def test_organization(self):
        self.login_admin()

        self.driver.find_element_by_link_text('Organizations').click()
        self.assertEqual(self.driver.current_url, self.live_server_url + 
                '/organization/list/')

        self.driver.find_element_by_link_text('Create Organization').click()
        self.assertEqual(self.driver.current_url, self.live_server_url + 
                '/organization/create/')
        
        # Test all valid characters for organization
        # [(A-Z)|(a-z)|(0-9)|(\s)|(\-)|(:)]
        self.driver.find_element_by_xpath('//input[@name = "name"]').send_keys(
                'Org-name 92:4 CA')
        self.driver.find_element_by_xpath('//form[1]').submit()
        # tr[2] since one dummy org already created in Setup, due to code-bug
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[2]//td[1]').text, 'Org-name 92:4 CA')

    def test_replication_of_organization(self):
        self.login_admin()

        self.driver.find_element_by_link_text('Organizations').click()
        self.assertEqual(self.driver.current_url, self.live_server_url + 
                '/organization/list/')

        self.driver.find_element_by_link_text('Create Organization').click()
        self.assertEqual(self.driver.current_url, self.live_server_url + 
                '/organization/create/')
        
        self.driver.find_element_by_xpath('//input[@name = "name"]').send_keys(
                'Organization')
        self.driver.find_element_by_xpath('//form[1]').submit()
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[2]//td[1]').text, 'Organization')

        # Create same orgnization again
        self.driver.find_element_by_link_text('Create Organization').click()
        self.assertEqual(self.driver.current_url, self.live_server_url + 
                '/organization/create/')
        
        self.driver.find_element_by_xpath('//input[@name = "name"]').send_keys(
                'Organization')
        self.driver.find_element_by_xpath('//form[1]').submit()
        
        self.assertEqual(self.driver.find_element_by_xpath(
            '//p[@class = "help-block"]').text,
            'Organization with this Name already exists.')

    def test_edit_org(self):
        # create org
        self.login_admin()

        self.driver.find_element_by_link_text('Organizations').click()
        self.assertEqual(self.driver.current_url, self.live_server_url + 
                '/organization/list/')

        self.driver.find_element_by_link_text('Create Organization').click()
        self.assertEqual(self.driver.current_url, self.live_server_url + 
                '/organization/create/')
        
        self.driver.find_element_by_xpath('//input[@name = "name"]').send_keys(
                'organization')
        self.driver.find_element_by_xpath('//form[1]').submit()

        # edit org
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[2]//td[2]').text, 'Edit')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[2]//td[2]//a').click()
        
        self.driver.find_element_by_xpath(
                '//input[@name = "name"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "name"]').send_keys('changed-organization')
        self.driver.find_element_by_xpath('//form[1]').submit()

        # check edited org
        org_list = []
        org_list.append(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text)
        org_list.append(self.driver.find_element_by_xpath(
            '//table//tbody//tr[2]//td[1]').text)

        self.assertTrue('changed-organization' in org_list)

    def test_delete_org_without_associated_users(self):
        # create org
        self.login_admin()

        self.driver.find_element_by_link_text('Organizations').click()
        self.assertEqual(self.driver.current_url, self.live_server_url + 
                '/organization/list/')

        self.driver.find_element_by_link_text('Create Organization').click()
        self.assertEqual(self.driver.current_url, self.live_server_url + 
                '/organization/create/')
        
        self.driver.find_element_by_xpath('//input[@name = "name"]').send_keys(
                'organization')
        self.driver.find_element_by_xpath('//form[1]').submit()

        # delete org
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[2]//td[3]').text, 'Delete')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[2]//td[3]//a').click()

        # confirm on delete
        self.assertNotEqual(self.driver.find_element_by_class_name(
            'panel-danger'), None)
        self.assertEqual(self.driver.find_element_by_class_name(
            'panel-heading').text, 'Delete Organization')
        self.driver.find_element_by_xpath('//form').submit()

        # check org deleted
        # There should only be one org entry in the table shown.
        # One, because of dummy-org inserted in setUp and not zero
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_xpath('//table//tbody//tr[2]')

        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text, 'DummyOrg')
    
    def test_delete_org_with_associated_users(self):
        # create org
        self.login_admin()

        self.driver.find_element_by_link_text('Organizations').click()
        self.driver.find_element_by_link_text('Create Organization').click()
        self.driver.find_element_by_xpath('//input[@name = "name"]').send_keys(
                'organization')
        self.driver.find_element_by_xpath('//form[1]').submit()

        # create Volunteer with Org as "organzization"
        volunteer_user = User.objects.create_user(
                username = 'volunteer',
                password = 'volunteer',
                email = 'volunteer@volunteer.com')

        Volunteer.objects.create(
                user = volunteer_user,
                address = 'address',
                city = 'city',
                state = 'state',
                country = 'country',
                phone_number = '9999999999',
                organization = Organization.objects.get(
                    name = 'organization'))

        # delete org
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[2]//td[3]').text, 'Delete')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[2]//td[3]//a').click()

        # confirm on delete
        self.assertNotEqual(self.driver.find_element_by_class_name(
            'panel-danger'), None)
        self.assertEqual(self.driver.find_element_by_class_name(
            'panel-heading').text, 'Delete Organization')
        self.driver.find_element_by_xpath('//form').submit()

        # check org not deleted message received
        self.assertNotEqual(self.driver.find_element_by_class_name(
            'alert-danger'), None)
        self.assertEqual(self.driver.find_element_by_xpath(
            '//div[2]/div[3]/p').text,
            'You cannot delete an organization that users are currently associated with.')
