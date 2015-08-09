from django.test import TestCase
from django.contrib.staticfiles.testing import LiveServerTestCase

from django.contrib.auth.models import User

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from volunteer.models import Volunteer
from organization.models import Organization #hack to pass travis,Bug in Code
from event.models import Event
from job.models import Job
from shift.models import Shift, VolunteerShift

class VolunteerReport(LiveServerTestCase):
    '''
    '''
    def setUp(self):
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
        super(VolunteerReport, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(VolunteerReport, self).tearDown()

    def login(self, credentials):
        self.driver.get(self.live_server_url + self.authentication_page)
        self.driver.find_element_by_id('id_login').send_keys(credentials['username'])
        self.driver.find_element_by_id('id_password').send_keys(credentials['password'])
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertEqual(self.driver.current_url,
                self.live_server_url + self.homepage)

    def register_event_utility(self):
        Event.objects.create(
                name = 'event',
                start_date = '2015-06-15',
                end_date = '2015-06-15')

    def register_job_utility(self):
        Job.objects.create(
                name = 'job',
                start_date = '2015-06-12',
                end_date = '2015-06-18',
                event = Event.objects.get(name = 'event'))

    def register_shift_utility(self):
        Shift.objects.create(
                date = '2015-06-15',
                start_time = '09:00',
                end_time = '15:00',
                max_volunteers ='6',
                job = Job.objects.get(name = 'job'))

    def log_hours_utility(self):
        VolunteerShift.objects.create(
                shift = Shift.objects.get(job__name = 'job'),
                volunteer = Volunteer.objects.get(user__username = 'volunteer'),
                start_time = '09:00',
                end_time = '12:00')

    def test_report_without_any_created_shifts(self):
        self.login({ 'username' : 'volunteer', 'password' : 'volunteer'})
        self.driver.find_element_by_link_text('Report').click()
        self.driver.find_element_by_xpath('//form').submit()
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-danger').text, 'Your criteria did not return any results.')

    def test_report_with_empty_fields(self):
        self.register_event_utility()
        self.register_job_utility()
        self.register_shift_utility()
        self.log_hours_utility()

        self.login({ 'username' : 'volunteer', 'password' : 'volunteer'})
        self.driver.find_element_by_link_text('Report').click()
        self.driver.find_element_by_xpath('//form').submit()

        total_no_of_shifts =  self.driver.find_element_by_xpath(
                '//div[2]/div[4]').text.split(' ')[10].strip('\nTotal')

        total_no_of_hours =  self.driver.find_element_by_xpath(
                '//div[2]/div[4]').text.split(' ')[-1].strip('\n')

        self.assertEqual(total_no_of_shifts, '1')
        self.assertEqual(total_no_of_hours, '3.0')

    def test_only_logged_shifts_appear_in_report(self):
        self.register_event_utility()
        self.register_job_utility()
        self.register_shift_utility()

        self.login({ 'username' : 'volunteer', 'password' : 'volunteer'})
        self.driver.find_element_by_link_text('Report').click()
        self.driver.find_element_by_xpath('//form').submit()
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-danger').text, 'Your criteria did not return any results.')

    def test_date_field(self):
        self.register_event_utility()
        self.register_job_utility()
        self.register_shift_utility()
        self.log_hours_utility()

        self.login({ 'username' : 'volunteer', 'password' : 'volunteer'})
        self.driver.find_element_by_link_text('Report').click()
        self.driver.find_element_by_xpath(
                '//input[@name = "date"]').send_keys('2015-06-15')
        self.driver.find_element_by_xpath('//form').submit()

        total_no_of_shifts =  self.driver.find_element_by_xpath(
                '//div[2]/div[4]').text.split(' ')[10].strip('\nTotal')

        total_no_of_hours =  self.driver.find_element_by_xpath(
                '//div[2]/div[4]').text.split(' ')[-1].strip('\n')

        self.assertEqual(total_no_of_shifts, '1')
        self.assertEqual(total_no_of_hours, '3.0')

        #incorrect date
        self.driver.find_element_by_xpath(
                '//input[@name = "date"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "date"]').send_keys('2015-07-15')
        self.driver.find_element_by_xpath('//form').submit()
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-danger').text, 'Your criteria did not return any results.')

    def test_event_field(self):
        self.register_event_utility()
        self.register_job_utility()
        self.register_shift_utility()
        self.log_hours_utility()

        self.login({ 'username' : 'volunteer', 'password' : 'volunteer'})
        self.driver.find_element_by_link_text('Report').click()
        self.driver.find_element_by_xpath(
                '//input[@name = "event_name"]').send_keys('event')
        self.driver.find_element_by_xpath('//form').submit()

        total_no_of_shifts =  self.driver.find_element_by_xpath(
                '//div[2]/div[4]').text.split(' ')[10].strip('\nTotal')

        total_no_of_hours =  self.driver.find_element_by_xpath(
                '//div[2]/div[4]').text.split(' ')[-1].strip('\n')

        self.assertEqual(total_no_of_shifts, '1')
        self.assertEqual(total_no_of_hours, '3.0')

        #incorrect event
        self.driver.find_element_by_xpath(
                '//input[@name = "event_name"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "event_name"]').send_keys('wrong-event')
        self.driver.find_element_by_xpath('//form').submit()
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-danger').text, 'Your criteria did not return any results.')

        #incorrect event format, should raise enter a valid value error
        self.driver.find_element_by_xpath(
                '//input[@name = "event_name"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "event_name"]').send_keys('!@#$')
        self.driver.find_element_by_xpath('//form').submit()
        self.assertEqual(self.driver.find_element_by_xpath(
            'html/body/div[2]/div[3]/form/fieldset/div[1]/div/p/strong').text, 'Enter a valid value.')

    def test_job_field(self):
        self.register_event_utility()
        self.register_job_utility()
        self.register_shift_utility()
        self.log_hours_utility()

        self.login({ 'username' : 'volunteer', 'password' : 'volunteer'})
        self.driver.find_element_by_link_text('Report').click()
        self.driver.find_element_by_xpath(
                '//input[@name = "job_name"]').send_keys('job')
        self.driver.find_element_by_xpath('//form').submit()

        total_no_of_shifts =  self.driver.find_element_by_xpath(
                '//div[2]/div[4]').text.split(' ')[10].strip('\nTotal')

        total_no_of_hours =  self.driver.find_element_by_xpath(
                '//div[2]/div[4]').text.split(' ')[-1].strip('\n')

        self.assertEqual(total_no_of_shifts, '1')
        self.assertEqual(total_no_of_hours, '3.0')

        #incorrect job
        self.driver.find_element_by_xpath(
                '//input[@name = "job_name"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "job_name"]').send_keys('wrongjob')
        self.driver.find_element_by_xpath('//form').submit()
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-danger').text, 'Your criteria did not return any results.')

        #incorrect job format, should raise enter a valid value error
        self.driver.find_element_by_xpath(
                '//input[@name = "job_name"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "job_name"]').send_keys('wrong-job')
        self.driver.find_element_by_xpath('//form').submit()
        self.assertEqual(self.driver.find_element_by_xpath(
            'html/body/div[2]/div[3]/form/fieldset/div[2]/div/p/strong').text, 'Enter a valid value.')


    def test_intersection_of_fields(self):
        self.register_event_utility()
        self.register_job_utility()
        self.register_shift_utility()
        self.log_hours_utility()

        self.login({ 'username' : 'volunteer', 'password' : 'volunteer'})
        self.driver.find_element_by_link_text('Report').click()
        self.driver.find_element_by_xpath(
                '//input[@name = "event_name"]').send_keys('event')
        self.driver.find_element_by_xpath(
                '//input[@name = "job_name"]').send_keys('job')
        self.driver.find_element_by_xpath(
                '//input[@name = "date"]').send_keys('2015-06-15')
        self.driver.find_element_by_xpath('//form').submit()

        total_no_of_shifts =  self.driver.find_element_by_xpath(
                '//div[2]/div[4]').text.split(' ')[10].strip('\nTotal')

        total_no_of_hours =  self.driver.find_element_by_xpath(
                '//div[2]/div[4]').text.split(' ')[-1].strip('\n')

        self.assertEqual(total_no_of_shifts, '1')
        self.assertEqual(total_no_of_hours, '3.0')

        # event, job correct and date incorrect
        self.driver.find_element_by_xpath(
                '//input[@name = "event_name"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "event_name"]').send_keys('event')
        self.driver.find_element_by_xpath(
                '//input[@name = "job_name"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "job_name"]').send_keys('job')
        self.driver.find_element_by_xpath(
                '//input[@name = "date"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "date"]').send_keys('2015-08-15')

        self.driver.find_element_by_xpath('//form').submit()
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-danger').text, 'Your criteria did not return any results.')
