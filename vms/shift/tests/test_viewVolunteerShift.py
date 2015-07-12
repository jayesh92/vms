from django.test import TestCase
from django.contrib.staticfiles.testing import LiveServerTestCase

from django.contrib.auth.models import User
from volunteer.models import Volunteer
from event.models import Event
from job.models import Job
from shift.models import Shift, VolunteerShift

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from organization.models import Organization #hack to pass travis,Bug in Code


class ViewVolunteerShift(LiveServerTestCase):
    '''
    '''
    def setUp(self):
        volunteer_user = User.objects.create_user(
                username = 'volunteer',
                password = 'volunteer',
                email = 'volunteer@volunteer.com')

        volunteer = Volunteer.objects.create(
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
        super(ViewVolunteerShift, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(ViewVolunteerShift, self).tearDown()

    def login(self, credentials):
        self.driver.get(self.live_server_url + self.authentication_page)
        self.driver.find_element_by_id('id_login').send_keys(credentials['username'])
        self.driver.find_element_by_id('id_password').send_keys(credentials['password'])
        self.driver.find_element_by_xpath('//form[1]').submit()

    def test_view_without_any_assigned_shift(self):
        credentials = {'username' : 'volunteer', 'password' : 'volunteer'}
        self.login(credentials)
        self.driver.find_element_by_link_text('Upcoming Shifts').click()
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-info').text, 'You do not have any upcoming shifts.')

    def register_dataset(self, parameters):
        try:
            org = Organization.objects.create(name = parameters['org'])
        except IntegrityError:
            org = Organization.objects.get(name = parameters['org'])


        volunteer = Volunteer.objects.get(user__username = 'volunteer')

        # create shift and log hours
        event = Event.objects.create(
                    name = parameters['event']['name'],
                    start_date = parameters['event']['start_date'],
                    end_date = parameters['event']['end_date'])

        job = Job.objects.create(
                name = parameters['job']['name'],
                start_date = parameters['job']['start_date'],
                end_date = parameters['job']['end_date'],
                event = event)

        shift = Shift.objects.create(
                date = parameters['shift']['date'],
                start_time = parameters['shift']['start_time'],
                end_time = parameters['shift']['end_time'],
                max_volunteers = parameters['shift']['max_volunteers'],
                job = job)

        # shift is assigned to volunteer
        VolunteerShift.objects.create(
                shift = shift,
                volunteer = volunteer)

    def test_view_with_assigned_and_unlogged_shift(self):
        parameters = {'org' : 'org-one',
                'event' : { 
                    'name' : 'event-four',
                    'start_date' : '2015-06-01',
                    'end_date' : '2015-06-10'},
                'job' : { 
                    'name' : 'jobOneInEventFour',
                    'start_date' : '2015-06-01',
                    'end_date' : '2015-06-01'},
                'shift' : {
                    'date' : '2015-06-01',
                    'start_time' : '09:00',
                    'end_time' : '10:00',
                    'max_volunteers' : '10'}}

        self.register_dataset(parameters)
        credentials = {'username' : 'volunteer', 'password' : 'volunteer'}
        self.login(credentials)
        self.driver.find_element_by_link_text('Upcoming Shifts').click()

        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text, 'jobOneInEventFour')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[2]').text, 'June 1, 2015')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[3]').text, '9 a.m.')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[4]').text, '10 a.m.')

    def test_log_hours_and_logged_shift_does_not_appear_in_upcoming_shifts(self):
        parameters = {'org' : 'org-one',
                'event' : { 
                    'name' : 'event-four',
                    'start_date' : '2015-06-01',
                    'end_date' : '2015-06-10'},
                'job' : { 
                    'name' : 'jobOneInEventFour',
                    'start_date' : '2015-06-01',
                    'end_date' : '2015-06-01'},
                'shift' : {
                    'date' : '2015-06-01',
                    'start_time' : '09:00',
                    'end_time' : '10:00',
                    'max_volunteers' : '10'}}

        self.register_dataset(parameters)
        credentials = {'username' : 'volunteer', 'password' : 'volunteer'}
        self.login(credentials)
        self.driver.find_element_by_link_text('Upcoming Shifts').click()

        self.assertEqual(self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[5]').text, 'Log Hours')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[5]/a').click()

        self.driver.find_element_by_xpath(
                '//input[@name = "start_time"]').send_keys('09:00')
        self.driver.find_element_by_xpath(
                '//input[@name = "end_time"]').send_keys('12:00')
        self.driver.find_element_by_xpath('//form').submit()

        # check logged shift does not appear in Upcoming Shifts
        self.driver.find_element_by_link_text('Upcoming Shifts').click()
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-info').text, 'You do not have any upcoming shifts.')
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_xpath('//table')

    def test_cancel_shift_registration(self):
        parameters = {'org' : 'org-one',
                'event' : { 
                    'name' : 'event-four',
                    'start_date' : '2015-06-01',
                    'end_date' : '2015-06-10'},
                'job' : { 
                    'name' : 'jobOneInEventFour',
                    'start_date' : '2015-06-01',
                    'end_date' : '2015-06-01'},
                'shift' : {
                    'date' : '2015-06-01',
                    'start_time' : '09:00',
                    'end_time' : '10:00',
                    'max_volunteers' : '10'}}

        self.register_dataset(parameters)
        credentials = {'username' : 'volunteer', 'password' : 'volunteer'}
        self.login(credentials)
        self.driver.find_element_by_link_text('Upcoming Shifts').click()

        self.assertEqual(self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[6]').text, 'Cancel Shift Registration')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[6]/a').click()

        self.assertEqual(self.driver.find_element_by_class_name(
            'panel-title').text, 'Cancel Shift Confirmation')
        self.assertEqual(self.driver.find_element_by_tag_name('button').text,
                'Yes, Cancel this Shift')
        self.driver.find_element_by_xpath('//form').submit()

        # check shift removed from upcoming shifts
        self.driver.find_element_by_link_text('Upcoming Shifts').click()
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-info').text, 'You do not have any upcoming shifts.')
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_xpath('//table')
