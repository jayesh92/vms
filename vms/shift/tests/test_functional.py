from django.test import TestCase
from django.contrib.staticfiles.testing import LiveServerTestCase

from django.contrib.auth.models import User
from administrator.models import Administrator

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from organization.models import Organization #hack to pass travis,Bug in Code


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

        # create an org prior to registration. Bug in Code
        # added to pass CI
        Organization.objects.create(
                name = 'DummyOrg')

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

    def test_landing_page_without_any_registered_volunteers(self):
        self.login_admin()
        self.driver.find_element_by_link_text('Manage Volunteer Shifts').click()
        self.assertEqual(self.driver.current_url,
                self.live_server_url + self.shift_page)
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_tag_name('tr')

    def test_landing_page_with_registered_volunteers(self):
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

    def test_events_page_with_no_events(self):
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

    def test_jobs_page_with_no_jobs(self):
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

    def test_assign_shifts_with_no_shifts(self):
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

    def test_assign_shifts_with_registered_shifts(self):
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

    def test_slots_remaining_in_shift(self):
        # register volunteers
        self.register_test_dataset()

        # create shift to assign, with only 1 volunteer required
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

        # open manage volunteer shift again to assign shift to volunteer two
        self.driver.find_element_by_link_text(
                'Manage Volunteer Shifts').click()
        self.assertEqual(self.driver.current_url,
                self.live_server_url +  self.shift_page)

        # volunteer-two does not have any registered shifts
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[2]//td[10]').text,
            'Manage Shifts')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[2]//td[10]//a').click()
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

        # arrived on jobs page
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[4]').text,
            'View Shifts')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[4]//a').click()

        # arrived on shifts page, but shift not shown since slots are already
        # filled.
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-info').text,
            'There are currently no shifts for the job name job.')
        # no unassigned shifts left for this job
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name('table')

    def test_cancel_assigned_shift(self):
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

        # arrived on jobs page
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[4]').text,
            'View Shifts')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[4]//a').click()

        # arrived on shifts page, assign shift to volunteer one
        slots_remaining_before_assignment = self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[5]').text
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

        # cancel assigned shift
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[5]').text,
            'Cancel Shift Registration')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[5]//a').click()
        self.assertNotEqual(self.driver.find_element_by_class_name(
            'panel-danger'), None)
        self.assertEqual(self.driver.find_element_by_class_name(
            'btn-danger').text, 'Yes, Cancel this Shift')
        self.driver.find_element_by_xpath('//form[1]').submit()

        # check cancelled shift reflects in volunteer shift details
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-info').text,
            'This volunteer does not have any upcoming shifts.')

        # check slots remaining increases by one, after cancellation of
        # assigned shift
        self.driver.find_element_by_link_text('Assign Shift').click()
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[4]').text,
            'View Jobs')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[4]//a').click()
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[4]').text,
            'View Shifts')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[4]//a').click()
        slots_after_cancellation = self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[5]').text
        self.assertEqual(slots_remaining_before_assignment,
                slots_after_cancellation)

    def test_assign_same_shift_to_volunteer_twice(self):
        # register volunteers
        self.register_test_dataset()

        # create shift to assign, with slots = 2
        shift = ['06/20/2015', '09:00', '15:00', '2']
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

        # arrived on jobs page
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[4]').text,
            'View Shifts')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[4]//a').click()

        # arrived on shifts page, assign shift to volunteer one
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[4]').text,
            'Assign Shift')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[4]//a').click()

        # confirm on shift assignment to volunteer-one
        self.driver.find_element_by_xpath('//form[1]').submit()
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name('alert-danger')

        # assign same shift to voluteer-one again
        # Check volunteer-one has one registered shift now
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text, 'job name')
        self.driver.find_element_by_link_text('Assign Shift').click()

        # events page
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name('alert-info')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[4]').text,
            'View Jobs')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[4]//a').click()

        # arrived on jobs page
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[4]').text,
            'View Shifts')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[4]//a').click()

        # arrived on shifts page, assign shift to volunteer one
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[4]').text,
            'Assign Shift')
        self.driver.find_element_by_xpath(
                '//table//tbody//tr[1]//td[4]//a').click()

        # confirm on shift assignment to volunteer-one
        self.driver.find_element_by_xpath('//form[1]').submit()

        # check error on assigning same shift to volunteer-one
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-danger').text,
            'Error\n\nThis user is already signed up for this shift. Please assign a different shift.')

