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


class ShiftHours(LiveServerTestCase):
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
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()
        super(ShiftHours, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(ShiftHours, self).tearDown()

    def login(self, credentials):
        self.driver.get(self.live_server_url + self.authentication_page)
        self.driver.find_element_by_id('id_login').send_keys(credentials['username'])
        self.driver.find_element_by_id('id_password').send_keys(credentials['password'])
        self.driver.find_element_by_xpath('//form[1]').submit()

    def test_view_without_any_unlogged_shift(self):
        self.login({'username' : 'volunteer', 'password' : 'volunteer'})
        self.driver.find_element_by_link_text('Shift Hours').click()

        volunteer_id = Volunteer.objects.get(user__username = 'volunteer').pk
        self.assertEqual(self.driver.current_url, self.live_server_url + 
                '/shift/view_hours/' + str(volunteer_id))

        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-info').text, 'You have not logged any hours.')

    def register_dataset(self, ):
        volunteer = Volunteer.objects.get(user__username = 'volunteer')

        # create shift and log hours
        event = Event.objects.create(
                    name = 'event',
                    start_date = '2015-06-15',
                    end_date = '2015-06-17')

        job = Job.objects.create(
                name = 'job',
                start_date = '2015-06-15',
                end_date = '2015-06-15',
                event = event)

        shift = Shift.objects.create(
                date = '2015-06-15',
                start_time = '09:00',
                end_time = '15:00',
                max_volunteers ='6',
                job = job)

        # logged hours from 12:00 to 13:00
        VolunteerShift.objects.create(
                shift = shift,
                volunteer = volunteer,
                start_time = '12:00',
                end_time = '13:00')

    def test_view_with_unlogged_shift(self):
        self.register_dataset()
        self.login({'username' : 'volunteer', 'password' : 'volunteer'})
        self.driver.find_element_by_link_text('Shift Hours').click()

        volunteer_id = Volunteer.objects.get(user__username = 'volunteer').pk
        self.assertEqual(self.driver.current_url, self.live_server_url + 
                '/shift/view_hours/' + str(volunteer_id))

        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text, 'job')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[2]').text, 'June 15, 2015')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[3]').text, 'noon')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[4]').text, '1 p.m.')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[5]').text, 'Edit Hours')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[6]').text, 'Clear Hours')

    def test_edit_hours(self):
        self.register_dataset()
        self.login({'username' : 'volunteer', 'password' : 'volunteer'})
        self.driver.find_element_by_link_text('Shift Hours').click()

        volunteer_id = Volunteer.objects.get(user__username = 'volunteer').pk
        self.assertEqual(self.driver.current_url, self.live_server_url + 
                '/shift/view_hours/' + str(volunteer_id))

        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[3]').text, 'noon')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[4]').text, '1 p.m.')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[5]').text, 'Edit Hours')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[5]//a').click()

        self.assertEqual(self.driver.find_element_by_xpath(
            'html/body/div[2]/div[2]/form/fieldset/legend').text,
            'Edit Shift Hours')
        self.driver.find_element_by_xpath(
                '//input[@name = "start_time"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "start_time"]').send_keys(
                        '15:00')

        self.driver.find_element_by_xpath(
                '//input[@name = "end_time"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "end_time"]').send_keys(
                        '20:00')
        self.driver.find_element_by_xpath('//form[1]').submit()
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[3]').text, '3 p.m.')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[4]').text, '8 p.m.')

    def test_end_hours_less_than_start_hours(self):
        self.register_dataset()
        self.login({'username' : 'volunteer', 'password' : 'volunteer'})
        self.driver.find_element_by_link_text('Shift Hours').click()

        volunteer_id = Volunteer.objects.get(user__username = 'volunteer').pk
        self.assertEqual(self.driver.current_url, self.live_server_url + 
                '/shift/view_hours/' + str(volunteer_id))

        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[3]').text, 'noon')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[4]').text, '1 p.m.')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[5]').text, 'Edit Hours')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[5]//a').click()

        self.assertEqual(self.driver.find_element_by_xpath(
            'html/body/div[2]/div[2]/form/fieldset/legend').text,
            'Edit Shift Hours')
        self.driver.find_element_by_xpath(
                '//input[@name = "start_time"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "start_time"]').send_keys(
                        '20:00')

        self.driver.find_element_by_xpath(
                '//input[@name = "end_time"]').clear()
        self.driver.find_element_by_xpath(
                '//input[@name = "end_time"]').send_keys(
                        '15:00')
        self.driver.find_element_by_xpath('//form[1]').submit()

        try:
            self.driver.find_element_by_class_name('alert-danger')
        except NoSuchElementException:
            raise Exception("End hours greater than start hours")

    def test_cancel_hours(self):
        self.register_dataset()
        self.login({'username' : 'volunteer', 'password' : 'volunteer'})
        self.driver.find_element_by_link_text('Shift Hours').click()

        volunteer_id = Volunteer.objects.get(user__username = 'volunteer').pk
        self.assertEqual(self.driver.current_url, self.live_server_url + 
                '/shift/view_hours/' + str(volunteer_id))

        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text, 'job')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[6]').text, 'Clear Hours')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[6]//a').click()

        self.assertEqual(self.driver.find_element_by_xpath(
            'html/body/div[2]/form/div/div[1]/h3').text,
            'Clear Shift Hours')
        self.driver.find_element_by_xpath('//form[1]').submit()

        with self.assertRaises(NoSuchElementException):
            self.assertEqual(self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[1]').text, 'job')
