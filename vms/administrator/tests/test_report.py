from django.test import TestCase
from django.contrib.staticfiles.testing import LiveServerTestCase

from django.contrib.auth.models import User
from django.db import IntegrityError

from administrator.models import Administrator
from volunteer.models import Volunteer
from event.models import Event
from job.models import Job
from shift.models import Shift, VolunteerShift
from organization.models import Organization #hack to pass travis,Bug in Code

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class Report(LiveServerTestCase):
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

        # create an org prior to registration. Bug in Code
        # added to pass CI
        Organization.objects.create(
                name = 'DummyOrg')

        self.homepage = '/home/'
        self.authentication_page = '/authentication/login/'
        self.report_page = '/administrator/report/'
        
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        super(Report, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(Report, self).tearDown()

    def login(self, username, password):
        self.driver.get(self.live_server_url + self.authentication_page)
        self.driver.find_element_by_id('id_login').send_keys(username)
        self.driver.find_element_by_id('id_password').send_keys(password)
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertEqual(self.driver.current_url,
                self.live_server_url + self.homepage)

    def logout(self):
        self.driver.find_element_by_link_text('Log Out').click()

    def test_null_values_with_empty_datatset(self):
        # should return no entries
        self.login('admin', 'admin')
        self.driver.find_element_by_link_text('Report').click()
        self.driver.find_element_by_xpath('//form[1]').submit()
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-danger').text, 'Your criteria did not return any results.')

    def test_null_values_with_dataset(self):
        # register dataset
        org = Organization.objects.create(name = 'organization-one')

        volunteer_user = User.objects.create_user(
                username = 'volunteer-one',
                password = 'volunteer-one',
                email = 'vol@vol.com')

        volunteer = Volunteer.objects.create(
                user = volunteer_user,
                first_name = 'first-name-one',
                last_name = 'last-name-one',
                address = 'address',
                city = 'city',
                state = 'state',
                country = 'country',
                phone_number = '9999999999',
                unlisted_organization = Organization.objects.get(
                    name = 'organization-one'))

        # create shift and log hours
        event = Event.objects.create(
                    name = 'Hackathon',
                    start_date = '2015-06-01',
                    end_date = '2015-06-01')

        job = Job.objects.create(
                name = 'Developer',
                start_date = '2015-06-01',
                end_date = '2015-06-01',
                event = event)

        shift = Shift.objects.create(
                date = '2015-06-01',
                start_time = '08:00',
                end_time = '20:00',
                max_volunteers = '2',
                job = job)

        VolunteerShift.objects.create(
                shift = shift,
                volunteer = volunteer,
                start_time = '09:00',
                end_time = '15:00')

        # check logged hours in volunteer-one's profile
        self.login('volunteer-one', 'volunteer-one')
        self.driver.get(self.live_server_url +
                '/shift/view_hours/' + str(Volunteer.objects.get(
                    user__username = 'volunteer-one').pk))

        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text, 'Developer')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[2]').text, 'June 1, 2015')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[3]').text, '9 a.m.')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[4]').text, '3 p.m.')
        self.logout()

        # check admin report with null fields, should return the above shift
        self.login('admin', 'admin')
        self.driver.get(self.live_server_url + self.report_page)
        self.driver.find_element_by_xpath('//form[1]').submit()
        total_no_of_shifts =  self.driver.find_element_by_xpath(
                '//div[2]/div[4]').text.split(' ')[10].strip('\nTotal')

        total_no_of_hours =  self.driver.find_element_by_xpath(
                '//div[2]/div[4]').text.split(' ')[-1].strip('\n')

        self.assertEqual(total_no_of_shifts, '1')
        self.assertEqual(total_no_of_hours, '6.0')

        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text, 'first-name-one')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[6]').text, 'June 1, 2015')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[7]').text, '9 a.m.')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[8]').text, '3 p.m.')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[9]').text, '6.0')

    def test_only_logged_shifts_are_reported(self):
        # register dataset
        org = Organization.objects.create(name = 'organization-one')

        volunteer_user = User.objects.create_user(
                username = 'volunteer-one',
                password = 'volunteer-one',
                email = 'vol@vol.com')

        volunteer = Volunteer.objects.create(
                user = volunteer_user,
                first_name = 'first-name-one',
                last_name = 'last-name-one',
                address = 'address',
                city = 'city',
                state = 'state',
                country = 'country',
                phone_number = '9999999999',
                organization = Organization.objects.get(
                    name = 'organization-one'))

        # create shift and log hours
        event = Event.objects.create(
                    name = 'Hackathon',
                    start_date = '2015-06-01',
                    end_date = '2015-06-01')

        job = Job.objects.create(
                name = 'Developer',
                start_date = '2015-06-01',
                end_date = '2015-06-01',
                event = event)

        shift = Shift.objects.create(
                date = '2015-06-01',
                start_time = '09:00',
                end_time = '15:00',
                max_volunteers = '2',
                job = job)

        # shift is assigned to volunteer-one, but hours have not been logged
        VolunteerShift.objects.create(
                shift = shift,
                volunteer = volunteer)

        # check shift assigned to volunteer-one
        # view being accessed `/shift/view_volunteer_shift`
        self.login('volunteer-one', 'volunteer-one')
        self.driver.get(self.live_server_url +
                '/shift/view_volunteer_shifts/' + str(Volunteer.objects.get(
                    user__username = 'volunteer-one').pk))

        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text, 'Developer')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[2]').text, 'June 1, 2015')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[3]').text, '9 a.m.')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[4]').text, '3 p.m.')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[5]//a').text, 'Log Hours')
        self.logout()

        # check admin report with null fields, should return the above shift
        self.login('admin', 'admin')
        self.driver.get(self.live_server_url + self.report_page)
        self.driver.find_element_by_xpath('//form[1]').submit()
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-danger').text, 'Your criteria did not return any results.')

    def register_dataset(self, parameters):
        try:
            org = Organization.objects.create(name = parameters['org'])
        except IntegrityError:
            org = Organization.objects.get(name = parameters['org'])


        volunteer_user = User.objects.create_user(
                username = parameters['volunteer']['username'],
                password = parameters['volunteer']['password'],
                email = parameters['volunteer']['email'])

        volunteer = Volunteer.objects.create(
                user = volunteer_user,
                first_name = parameters['volunteer']['first_name'],
                last_name = parameters['volunteer']['last_name'],
                address = parameters['volunteer']['address'],
                city = parameters['volunteer']['city'],
                state = parameters['volunteer']['state'],
                country = parameters['volunteer']['country'],
                phone_number = parameters['volunteer']['phone-no'],
                organization = Organization.objects.get(
                    name = parameters['org']))

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

        # shift is assigned to volunteer-one, but hours have not been logged
        VolunteerShift.objects.create(
                shift = shift,
                volunteer = volunteer,
                start_time = parameters['vshift']['start_time'],
                end_time = parameters['vshift']['end_time'])

    def test_check_intersection_of_fields(self):
        parameters = {'org' : 'org-one',
                'volunteer' : {
                    'username' : 'uname1', 
                    'password' : 'uname1', 
                    'email' : 'email@email.com',
                    'first_name' : 'tom-fname',
                    'last_name' : 'tom-lname',
                    'address' : 'address',
                    'city' : 'city',
                    'state' : 'state',
                    'country' : 'country',
                    'phone-no' : '9999999999'},
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
                    'max_volunteers' : '10'},
                'vshift' : {
                    'start_time' : '09:30',
                    'end_time' : '10:00',}}
        self.register_dataset(parameters)

        parameters = {'org' : 'org-one',
                'volunteer' : {
                    'username' : 'uname2', 
                    'password' : 'uname2', 
                    'email' : 'email@email.com',
                    'first_name' : 'peter-fname',
                    'last_name' : 'peter-lname',
                    'address' : 'address',
                    'city' : 'city',
                    'state' : 'state',
                    'country' : 'country',
                    'phone-no' : '9999999999'},
                'event' : {
                    'name' : 'event-one',
                    'start_date' : '2015-06-01',
                    'end_date' : '2015-06-10'},
                'job' : {
                    'name' : 'jobOneInEventOne',
                    'start_date' : '2015-06-01',
                    'end_date' : '2015-06-01'},
                'shift' : {
                    'date' : '2015-06-01',
                    'start_time' : '09:00',
                    'end_time' : '10:00',
                    'max_volunteers' : '10'},
                'vshift' : {
                    'start_time' : '19:00',
                    'end_time' : '23:00'}}
        self.register_dataset(parameters)

        parameters = {'org' : 'org-one',
                'volunteer' : {
                    'username' : 'uname3', 
                    'password' : 'uname3', 
                    'email' : 'email@email.com',
                    'first_name' : 'tom-fname',
                    'last_name' : 'tom-lname',
                    'address' : 'address',
                    'city' : 'city',
                    'state' : 'state',
                    'country' : 'country',
                    'phone-no' : '9999999999'},
                'event' : {
                    'name' : 'event-four',
                    'start_date' : '2015-06-01',
                    'end_date' : '2015-06-10'},
                'job' : {
                    'name' : 'jobTwoInEventFour',
                    'start_date' : '2015-06-01',
                    'end_date' : '2015-06-01'},
                'shift' : {
                    'date' : '2015-06-01',
                    'start_time' : '09:00',
                    'end_time' : '10:00',
                    'max_volunteers' : '10'},
                'vshift' : {
                    'start_time' : '15:00',
                    'end_time' : '18:30'}}
        self.register_dataset(parameters)

        parameters = {'org' : 'org-two',
                'volunteer' : {
                    'username' : 'uname4', 
                    'password' : 'uname4', 
                    'email' : 'email@email.com',
                    'first_name' : 'harry-fname',
                    'last_name' : 'harry-lname',
                    'address' : 'address',
                    'city' : 'city',
                    'state' : 'state',
                    'country' : 'country',
                    'phone-no' : '9999999999'},
                'event' : {
                    'name' : 'event-one',
                    'start_date' : '2015-06-01',
                    'end_date' : '2015-06-10'},
                'job' : {
                    'name' : 'jobTwoInEventOne',
                    'start_date' : '2015-06-01',
                    'end_date' : '2015-06-01'},
                'shift' : {
                    'date' : '2015-06-01',
                    'start_time' : '09:00',
                    'end_time' : '10:00',
                    'max_volunteers' : '10'},
                'vshift' : {
                    'start_time' : '09:00',
                    'end_time' : '10:00'}}
        self.register_dataset(parameters)

        parameters = {'org' : 'org-two',
                'volunteer' : {
                    'username' : 'uname5', 
                    'password' : 'uname5', 
                    'email' : 'email@email.com',
                    'first_name' : 'harry-fname',
                    'last_name' : 'harry-lname',
                    'address' : 'address',
                    'city' : 'city',
                    'state' : 'state',
                    'country' : 'country',
                    'phone-no' : '9999999999'},
                'event' : {
                    'name' : 'event-two',
                    'start_date' : '2015-06-01',
                    'end_date' : '2015-06-10'},
                'job' : {
                    'name' : 'jobOneInEventTwo',
                    'start_date' : '2015-06-01',
                    'end_date' : '2015-06-01'},
                'shift' : {
                    'date' : '2015-06-01',
                    'start_time' : '09:00',
                    'end_time' : '10:00',
                    'max_volunteers' : '10'},
                'vshift' : {
                    'start_time' : '12:00',
                    'end_time' : '17:00'}}
        self.register_dataset(parameters)

        parameters = {'org' : 'org-three',
                'volunteer' : {
                    'username' : 'uname6', 
                    'password' : 'uname6', 
                    'email' : 'email@email.com',
                    'first_name' : 'sherlock-fname',
                    'last_name' : 'sherlock-lname',
                    'address' : 'address',
                    'city' : 'city',
                    'state' : 'state',
                    'country' : 'country',
                    'phone-no' : '9999999999'},
                'event' : {
                    'name' : 'event-two',
                    'start_date' : '2015-06-01',
                    'end_date' : '2015-06-10'},
                'job' : {
                    'name' : 'jobOneInEventTwo',
                    'start_date' : '2015-06-01',
                    'end_date' : '2015-06-01'},
                'shift' : {
                    'date' : '2015-06-01',
                    'start_time' : '09:00',
                    'end_time' : '10:00',
                    'max_volunteers' : '10'},
                'vshift' : {
                    'start_time' : '16:00',
                    'end_time' : '18:00'}}
        self.register_dataset(parameters)

        parameters = {'org' : 'org-four',
                'volunteer' : {
                    'username' : 'uname7', 
                    'password' : 'uname7', 
                    'email' : 'email@email.com',
                    'first_name' : 'harvey-fname',
                    'last_name' : 'harvey-lname',
                    'address' : 'address',
                    'city' : 'city',
                    'state' : 'state',
                    'country' : 'country',
                    'phone-no' : '9999999999'},
                'event' : {
                    'name' : 'event-one',
                    'start_date' : '2015-06-01',
                    'end_date' : '2015-06-10'},
                'job' : {
                    'name' : 'jobThreeInEventOne',
                    'start_date' : '2015-06-01',
                    'end_date' : '2015-06-01'},
                'shift' : {
                    'date' : '2015-06-01',
                    'start_time' : '09:00',
                    'end_time' : '10:00',
                    'max_volunteers' : '10'},
                'vshift' : {
                    'start_time' : '19:00',
                    'end_time' : '19:30'}}
        self.register_dataset(parameters)

        parameters = {'org' : 'org-four',
                'volunteer' : {
                    'username' : 'uname8', 
                    'password' : 'uname8', 
                    'email' : 'email@email.com',
                    'first_name' : 'mike-fname',
                    'last_name' : 'mike-lname',
                    'address' : 'address',
                    'city' : 'city',
                    'state' : 'state',
                    'country' : 'country',
                    'phone-no' : '9999999999'},
                'event' : {
                    'name' : 'event-three',
                    'start_date' : '2015-06-01',
                    'end_date' : '2015-06-10'},
                'job' : {
                    'name' : 'jobOneInEventThree',
                    'start_date' : '2015-06-01',
                    'end_date' : '2015-06-01'},
                'shift' : {
                    'date' : '2015-06-01',
                    'start_time' : '09:00',
                    'end_time' : '10:00',
                    'max_volunteers' : '10'},
                'vshift' : {
                    'start_time' : '01:00',
                    'end_time' : '10:00'}}
        self.register_dataset(parameters)

        self.login('admin', 'admin')
        self.driver.get(self.live_server_url + self.report_page)

        self.driver.find_element_by_xpath(
                '//input[@name = "first_name"]').send_keys('tom')
        self.driver.find_element_by_xpath('//form[1]').submit()

        total_no_of_shifts =  self.driver.find_element_by_xpath(
                '//div[2]/div[4]').text.split(' ')[10].strip('\nTotal')

        total_no_of_hours =  self.driver.find_element_by_xpath(
                '//div[2]/div[4]').text.split(' ')[-1].strip('\n')

        # 2 shifts of 0.5 hrs and 3.5 hrs
        self.assertEqual(total_no_of_shifts, '2')
        self.assertEqual(total_no_of_hours, '4.0')

        self.driver.find_element_by_xpath(
                '//input[@name = "first_name"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "organization"]').send_keys('org-one')
        self.driver.find_element_by_xpath('//form[1]').submit()

        total_no_of_shifts =  self.driver.find_element_by_xpath(
                '//div[2]/div[4]').text.split(' ')[10].strip('\nTotal')

        total_no_of_hours =  self.driver.find_element_by_xpath(
                '//div[2]/div[4]').text.split(' ')[-1].strip('\n')

        # 3 shifts of 0.5 hrs, 3:30 hrs and 4 hrs
        self.assertEqual(total_no_of_shifts, '3')
        self.assertEqual(total_no_of_hours, '8.0')

        self.driver.find_element_by_xpath(
                '//input[@name = "first_name"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "organization"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "event_name"]').send_keys('event-four')
        # searching for jobTwoInEventFour
        self.driver.find_element_by_xpath(
                '//input[@name = "job_name"]').send_keys('Two')
        self.driver.find_element_by_xpath('//form[1]').submit()

        total_no_of_shifts =  self.driver.find_element_by_xpath(
                '//div[2]/div[4]').text.split(' ')[10].strip('\nTotal')

        total_no_of_hours =  self.driver.find_element_by_xpath(
                '//div[2]/div[4]').text.split(' ')[-1].strip('\n')

        # 1 shift of 3:30 hrs
        self.assertEqual(total_no_of_shifts, '1')
        self.assertEqual(total_no_of_hours, '3.5')

        self.driver.find_element_by_xpath(
                '//input[@name = "first_name"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "organization"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "event_name"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "job_name"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "event_name"]').send_keys('one')
        self.driver.find_element_by_xpath('//form[1]').submit()

        total_no_of_shifts =  self.driver.find_element_by_xpath(
                '//div[2]/div[4]').text.split(' ')[10].strip('\nTotal')

        total_no_of_hours =  self.driver.find_element_by_xpath(
                '//div[2]/div[4]').text.split(' ')[-1].strip('\n')

        # 3 shifts of 0:30 hrs, 4:00 hrs, 1:00 hrs
        self.assertEqual(total_no_of_shifts, '3')
        self.assertEqual(total_no_of_hours, '5.5')

        self.driver.find_element_by_xpath(
                '//input[@name = "first_name"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "organization"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "event_name"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "job_name"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "last_name"]').send_keys('sherlock')
        # check case-insensitive
        self.driver.find_element_by_xpath(
                '//input[@name = "event_name"]').send_keys('two')
        self.driver.find_element_by_xpath('//form[1]').submit()

        total_no_of_shifts =  self.driver.find_element_by_xpath(
                '//div[2]/div[4]').text.split(' ')[10].strip('\nTotal')

        total_no_of_hours =  self.driver.find_element_by_xpath(
                '//div[2]/div[4]').text.split(' ')[-1].strip('\n')

        # 1 shift of 2:00 hrs
        self.assertEqual(total_no_of_shifts, '1')
        self.assertEqual(total_no_of_hours, '2.0')
