from django.test import TestCase, Client

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from models import *

class TestOrganization(TestCase):
	"""
	This class serves to creating a Test Suite for testing the organization model.
	The methods in this class test insertion of valid values, errors in duplicate entries and
	Validators for fields of Organization class
	"""
	def setUp(self):
		org = Organization(name='LinkedIn',location='blr')
		org.save()

	def test_insertion(self):
		self.assertEqual(Organization.objects.filter(name='LinkedIn').count(), 1)

	def test_duplication(self):
		self.assertRaises(IntegrityError, lambda: Organization.objects.create(name='LinkedIn',location='blr'))
	
	def test_name(self):
		# To test if org name does not allow numbers or special characters
		org = Organization(name='LinkedIn123',location='blr')
		with self.assertRaises(ValidationError):
			if org.full_clean():
				org.save()
		self.assertEqual(Organization.objects.filter(name='LinkedIn123',location='blr').count(), 0)

	def test_location(self):
		org = Organization(name='LinkedInTest',location='Bangalore123')
		with self.assertRaises(ValidationError):
			if org.full_clean():
				org.save()
		self.assertEqual(Organization.objects.filter(name='LinkedInTest').count(), 0)


class TestAdmins(TestCase):
	"""
	This class serves to creating a Test Suite for testing the AdminProfile model.
	The methods in this class test insertion of valid values, errors in duplicate entries,
	Foregin Key relationship with Organization class
	Validators for fields of AdminProfile class
	"""
	def setUp(self):
		Organization.objects.create(name='LinkedIn',location='Bangalore')
		user = User.objects.create_user(first_name='Jayesh',last_name='Lahori',email='jlahori92@gmail.com',username='jlahori',password='password')
		AdminProfile.objects.create(user=user,address='IIIT-H',location='Hyderabad',state='Andhra Pradesh',organization=Organization.objects.get(name='LinkedIn'),phone='9581845730')

	def test_insertion(self):
		self.assertEqual(1,AdminProfile.objects.filter(user__username='jlahori').count())

	def test_duplication(self):
		self.assertRaises(IntegrityError, lambda:  AdminProfile.objects.create(user=User.objects.get(username='jlahori'),address='IIIT-H',location='Hyderabad',state='Andhra Pradesh',organization=Organization.objects.get(name='LinkedIn'),phone='9581845730'))

	def test_location(self):
		# To test if city(location) name does not allow numbers or special characters
		profile = AdminProfile(user=User.objects.create_user(first_name='Jayesh',last_name='Lahori',email='jlahori92@gmail.com',username='jlahori_test2',password='password'),address='IIIT-H',location='Hyderabad123!@#',state='Andhra Pradesh',organization=Organization.objects.get(name='LinkedIn'),phone='9581845730')
		with self.assertRaises(ValidationError):
			if profile.full_clean():
				profile.save()
		self.assertEqual(0,AdminProfile.objects.filter(user__username='jlahori_test2').count())

	def test_state(self):
		# To test if state does not allow numbers or special characters
		profile = AdminProfile(user=User.objects.create_user(first_name='Jayesh',last_name='Lahori',email='jlahori92@gmail.com',username='jlahori_test2',password='password'),address='IIIT-H',location='Hyderabad',state='Andhra Pradesh 123 !@#',organization=Organization.objects.get(name='LinkedIn'),phone='9581845730')
		with self.assertRaises(ValidationError):
			if profile.full_clean():
				profile.save()
		self.assertEqual(0,AdminProfile.objects.filter(user__username='jlahori_test2').count())


	def test_phone(self):
		# To test if phone numbers does not allow anything except 10 numbers
		profile = AdminProfile(user=User.objects.create_user(first_name='Jayesh',last_name='Lahori',email='jlahori92@gmail.com',username='jlahori_test2',password='password'),address='IIIT-H',location='Hyderabad',state='Andhra Pradesh',organization=Organization.objects.get(name='LinkedIn'),phone='919581845730')
		with self.assertRaises(ValidationError):
			if profile.full_clean():
				profile.save()
		self.assertEqual(0,AdminProfile.objects.filter(user__username='jlahori_test2').count())
	
	def test_organization_foreign_key(self):
		# To test only registered organizations should be allowed as valid entries
		org=Organization(name='Google',location='Hyderabad')
		profile = AdminProfile(user=User.objects.create_user(first_name='Jayesh',last_name='Lahori',email='jlahori92@gmail.com',username='jlahori_test2',password='password'),address='IIIT-H',location='Hyderabad',state='Andhra Pradesh',organization=org,phone='9581845730')
		with self.assertRaises(ValidationError):
			if profile.full_clean():
				profile.save()
		self.assertEqual(0,AdminProfile.objects.filter(user__username='jlahori_test2').count())

class TestEvent(TestCase):
	"""
	This class serves to creating a Test Suite for testing the event model.
	The methods in this class test insertion of valid values, errors in duplicate entries and
	Validators for fields of Event class
	"""
	def setUp(self):
		Event.objects.create(eventName='event1',noOfVolunteersRequired=5,startDate='2015-05-05 05:05:05',endDate='2015-05-05 05:05:05')
	
	def test_insertion(self):
		self.assertEqual(1,Event.objects.filter(eventName='event1').count())
	
	def test_duplication(self):
		self.assertRaises(IntegrityError, lambda: Event.objects.create(eventName='event1',noOfVolunteersRequired=5,startDate='2015-05-05 05:05:05',endDate='2015-05-05 05:05:05'))

	def test_noOfVolunteersRequired_zero(self):
		# To test if noOfVolunteersRequired does not allow 0 as valid entry
		event = Event(eventName='event1_test', noOfVolunteersRequired=0, startDate='2015-05-05 05:05:05', endDate='2015-05-05 05:05:05')
		with self.assertRaises(ValidationError):
			if event.full_clean():
				event.save()
		self.assertEqual(0,Event.objects.filter(eventName='event1_test').count())
	
	def test_noOfVolunteersRequired_negative(self):
		# To test if noOfVolunteersRequired does not allow -ve as valid entry
		event = Event(eventName='event1_test', noOfVolunteersRequired=-1, startDate='2015-05-05 05:05:05', endDate='2015-05-05 05:05:05')
		with self.assertRaises(ValidationError):
			if event.full_clean():
				event.save()
		self.assertEqual(0,Event.objects.filter(eventName='event1_test').count())

	def test_startTime(self):
		# To test if startTime format follows YYYY-MM-DD HH:MM:SS does not 0 as valid entry
		event = Event(eventName='event1_test', noOfVolunteersRequired=1, startDate='2015-05-05 05-05-05', endDate='2015-05-05 05:05:05')
		with self.assertRaises(ValidationError):
			if event.full_clean():
				event.save()
		self.assertEqual(0,Event.objects.filter(eventName='event1_test').count())

	def test_endTime(self):
		# To test if endTime format follows YYYY-MM-DD HH:MM:SS does not 0 as valid entry
		event = Event(eventName='event1_test', noOfVolunteersRequired=-1, startDate='2015-05-05 05:05:05', endDate='2015-05-05 25:05:05')
		with self.assertRaises(ValidationError):
			if event.full_clean():
				event.save()
		self.assertEqual(0,Event.objects.filter(eventName='event1_test').count())

class TestJob(TestCase):
	"""
	This class serves to creating a Test Suite for testing the Job model.
	The methods in this class test insertion of valid values, errors in duplicate entries(multiple_unique in this case),
	Foreign key relationship with Event class
	Validators for fields of Jobs class
	"""
	def setUp(self):
		event = Event.objects.create(eventName='event1',noOfVolunteersRequired=5,startDate='2015-05-05 05:05:05',endDate='2015-05-05 05:05:05')
		Job.objects.create(event=event, jobName='Test Job Name', jobDescription='Test Job Description', noOfVolunteersRequired=5,startDate='2015-05-05 05:05:05',endDate='2015-05-05 05:05:05')
	
	def test_insertion(self):
		self.assertEqual(1,Job.objects.filter(event__eventName='event1').count())

	def test_duplication(self):
		self.assertRaises(IntegrityError, lambda: Job.objects.create(event=Event.objects.get(eventName='event1'), jobName='Test Job Name', jobDescription='Test Job Description', noOfVolunteersRequired=5, startDate='2015-05-05 05:05:05', endDate='2015-05-05 05:05:05'))
	
	def test_event_foreign_key(self):
		# To test if only registered events are allowed in creation of jobs
		event = Event(eventName='event2',noOfVolunteersRequired=5,startDate='2015-05-05 05:05:05',endDate='2015-05-05 05:05:05')
		job = Job(event=event, jobName='Test Job Name', jobDescription='Test Job Description', noOfVolunteersRequired=5,startDate='2015-05-05 05:05:05',endDate='2015-05-05 05:05:05')
		with self.assertRaises(ValidationError):
			if job.full_clean():
				job.save()
		self.assertEqual(0,Job.objects.filter(event__eventName='event2').count())

class TestShift(TestCase):
	"""
	This class serves to creating a Test Suite for testing the Shift model.
	The methods in this class test insertion of valid values, errors in duplicate entries(multiple_unique in this case),
	Foreign key relationship with volunteer, event, job models
	Validators for fields of Organization class
	"""
	def setUp(self):
		event = Event.objects.create(eventName='event1',noOfVolunteersRequired=5,startDate='2015-05-05 05:05:05',endDate='2015-05-05 05:05:05')
		user = User.objects.create_user(first_name='Jayesh',last_name='Lahori',email='jlahori92@gmail.com',username='jlahori',password='password')
		profile = AdminProfile.objects.create(user=user,address='IIIT-H',location='Hyderabad',state='Andhra Pradesh',organization=Organization.objects.create(name='LinkedIn', location='blr'),phone='9581845730')
		job = Job.objects.create(event=event, jobName='Test Job Name', jobDescription='Test Job Description', noOfVolunteersRequired=5, startDate='2015-05-05 05:05:05', endDate='2015-05-05 05:05:05')
		Shift.objects.create(event=event, volunteer=profile, job=job, hours=1)
	
	def test_insertion(self):
		self.assertEqual(1,Shift.objects.filter(event__eventName='event1',volunteer__user__username='jlahori',job__event__eventName='event1').count())
	
	def test_duplication(self):
		self.assertRaises(IntegrityError, lambda: Shift.objects.create(event=Event.objects.get(eventName='event1'), job=Job.objects.get(jobName='Test Job Name',event__eventName='event1'), volunteer=AdminProfile.objects.get(user__username='jlahori'),hours=2 ))

	def test_event_foreign_key(self):
		# To test if only registered events are allowed in creation of shifts
		event = Event(eventName='event2',noOfVolunteersRequired=5,startDate='2015-05-05 05:05:05',endDate='2015-05-05 05:05:05')
		shift = Shift(event=event, volunteer=AdminProfile.objects.get(user__username='jlahori'), job=Job.objects.get(event__eventName='event1'), hours=1)
		with self.assertRaises(ValidationError):
			if shift.full_clean():
				job.save()
		self.assertEqual(0,Shift.objects.filter(event__eventName='event2').count())

	def test_volunteer_foreign_key(self):
		# To test if only registered volunteers are allowed in creation of shifts
		previousCount = Shift.objects.filter(event__eventName='event1').count()
		profile = AdminProfile(user=User(first_name='Jayesh',last_name='Lahori',email='jlahori92@gmail.com',username='jlahori_test',password='password'),address='IIIT-H',location='Hyderabad',state='Andhra Pradesh',phone='9581845730',organization=Organization(name='Google', location='hyderabad'))
		shift = Shift(event=Event.objects.get(eventName='event1'), volunteer=profile, job=Job.objects.get(event__eventName='event1'), hours=1)
		with self.assertRaises(ValidationError):
			if shift.full_clean():
				shift.save()
		self.assertEqual(previousCount, Shift.objects.filter(event__eventName='event1').count())

class TestRegisterView(TestCase):
	"""
	This class serves to creating a Test Suite for testing the register view.
	The methods in this class test insertion of valid values, asserting errors in null entries
	"""
	def test_invalid_value(self):
		c = Client()
		response = c.post('/AdminUnit/register/', {'firstname' : 'test', 'lastname' : 'test', 'email' : 'test', 'username' : 'test',
			'password' : 'test', 'password2' : 'test', 'address' : 'test', 'location' : 'test', 'state' : 'test', 'organization' : 'test',
			'phone' : '919581845730'})
		self.assertEqual(200, response.status_code)
		self.assertEqual(response.context['userForm']['email'].errors, ['Enter a valid email address.'])
		self.assertEqual(response.context['adminProfileForm']['organization'].errors,
				['Select a valid choice. That choice is not one of the available choices.'])
		self.assertEqual(response.context['adminProfileForm']['phone'].errors, ['Enter a valid value.'])

	def test_null_value(self):
		c = Client()
		response = c.post('/AdminUnit/register/', {})
		self.assertEqual(200, response.status_code)
		self.assertEqual(response.context['adminProfileForm']['phone'].errors, ["This field is required."])
		self.assertEqual(response.context['adminProfileForm']['organization'].errors, ["This field is required."])
		self.assertEqual(response.context['adminProfileForm']['address'].errors, ["This field is required."])
		self.assertEqual(response.context['adminProfileForm']['location'].errors, ["This field is required."])
		self.assertEqual(response.context['adminProfileForm']['state'].errors, ["This field is required."])
		self.assertEqual(response.context['userForm']['firstname'].errors, ["This field is required."])
		self.assertEqual(response.context['userForm']['lastname'].errors, ["This field is required."])
		self.assertEqual(response.context['userForm']['username'].errors, ["This field is required."])
		self.assertEqual(response.context['userForm']['email'].errors, ["This field is required."])
		self.assertEqual(response.context['userForm']['password'].errors, ["This field is required."])
		self.assertEqual(response.context['userForm']['password2'].errors, ["This field is required."])

class TestEventView(TestCase):
	"""
	This class serves to creating a Test Suite for testing the Create Event View.
	The methods in this class test login_required decorator, insertion of valid values, asserting errors in null entries
	"""
	def test_login_required(self):
		c = Client()
		response = c.post('/AdminUnit/job/',{})
		
		self.assertNotEqual(200, response.status_code)

	def test_invalid_value(self):
		c = Client()
		user = User.objects.create_user(first_name='Jayesh',last_name='Lahori',email='jlahori92@gmail.com',username='jlahori',password='password')
		profile = AdminProfile.objects.create(user=user,address='IIIT-H',location='Hyderabad',state='Andhra Pradesh',organization=Organization.objects.create(name='LinkedIn', location='blr'),phone='9581845730')
		self.assertEqual(1, AdminProfile.objects.filter(user__username='jlahori').count())

		c.login(username='jlahori', password='password')

		Event.objects.create(eventName='test_event', noOfVolunteersRequired=10, startDate='2014-05-05 05:05:05', endDate='2014-05-05 05:05:05')
		self.assertEqual(1, Event.objects.filter(eventName='test_event').count())

		response = c.post('/AdminUnit/event/', {'eventName' : 'test_event', 'noOfVolunteersRequired' : '-1',
			'startDate' : '2014-05-05 05-05-05', 'endDate' : '05-10-2014 05:05:05'})

		self.assertEqual(200, response.status_code)
		self.assertEqual(response.context['eventForm']['eventName'].errors, ['Event with this EventName already exists.'])
		self.assertEqual(response.context['eventForm']['noOfVolunteersRequired'].errors, ['Enter a whole number.'])
		self.assertEqual(response.context['eventForm']['startDate'].errors, ['Enter a valid date/time.'])
		self.assertEqual(response.context['eventForm']['endDate'].errors, ['Enter a valid date/time.'])
	
	def test_null_value(self):
		c = Client()
		user = User.objects.create_user(first_name='Jayesh',last_name='Lahori',email='jlahori92@gmail.com',username='jlahori',password='password')
		profile = AdminProfile.objects.create(user=user,address='IIIT-H',location='Hyderabad',state='Andhra Pradesh',organization=Organization.objects.create(name='LinkedIn', location='blr'),phone='9581845730')
		c.login(username='jlahori', password='password')

		Event.objects.create(eventName='test_event', noOfVolunteersRequired=10, startDate='2014-05-05 05:05:05', endDate='2014-05-05 05:05:05')
		self.assertEqual(1, Event.objects.filter(eventName='test_event').count())

		response = c.post('/AdminUnit/event/', {})
		self.assertEqual(200, response.status_code)
		self.assertEqual(response.context['eventForm']['eventName'].errors, ['This field is required.'])
		self.assertEqual(response.context['eventForm']['noOfVolunteersRequired'].errors, ['This field is required.'])
		self.assertEqual(response.context['eventForm']['startDate'].errors, ['This field is required.'])
		self.assertEqual(response.context['eventForm']['endDate'].errors, ['This field is required.'])

class TestJobView(TestCase):
	"""
	This class serves to creating a Test Suite for testing the Create Job View.
	The methods in this class test login_required decorator, insertion of valid values, asserting errors in null entries,
	Check unique_together property of Job Event
	"""
	def test_login_required(self):
		c = Client()
		response = c.post('/AdminUnit/job/',{})
		
		self.assertNotEqual(200, response.status_code)

	def test_invalid_value(self):
		Event.objects.create(eventName='test_event_1', noOfVolunteersRequired=10, startDate='2014-05-05 05:05:05', endDate='2014-05-05 05:05:05')
		self.assertEqual(1, Event.objects.filter(eventName='test_event_1').count())

		c = Client()
		user = User.objects.create_user(first_name='Jayesh',last_name='Lahori',email='jlahori92@gmail.com',username='jlahori',password='password')
		profile = AdminProfile.objects.create(user=user,address='IIIT-H',location='Hyderabad',state='Andhra Pradesh',organization=Organization.objects.create(name='LinkedIn', location='blr'),phone='9581845730')
		self.assertEqual(1, AdminProfile.objects.filter(user__username='jlahori').count())
		c.login(username='jlahori', password='password')

		response = c.post('/AdminUnit/job/',{'event' : 'test_event_2', 'jobName' : 'test_jobName',
			'jobDescription' : 'test_jobDescription', 'startDate' : '2014-05-05 05-05-05', 'endDate' : '05-10-2014 05:05:05'})

		self.assertEqual(200, response.status_code)
		self.assertEqual(response.context['jobsForm']['event'].errors, ['Select a valid choice. That choice is not one of the available choices.'])
		self.assertEqual(response.context['jobsForm']['startDate'].errors, ['Enter a valid date/time.'])
		self.assertEqual(response.context['jobsForm']['endDate'].errors, ['Enter a valid date/time.'])

	def test_null_value(self):
		c = Client()
		user = User.objects.create_user(first_name='Jayesh',last_name='Lahori',email='jlahori92@gmail.com',username='jlahori',password='password')
		profile = AdminProfile.objects.create(user=user,address='IIIT-H',location='Hyderabad',state='Andhra Pradesh',organization=Organization.objects.create(name='LinkedIn', location='blr'),phone='9581845730')
		self.assertEqual(1, AdminProfile.objects.filter(user__username='jlahori').count())
		c.login(username='jlahori', password='password')

		response = c.post('/AdminUnit/job/',{})

		self.assertEqual(200, response.status_code)
		self.assertEqual(response.context['jobsForm']['event'].errors, ['This field is required.'])
		self.assertEqual(response.context['jobsForm']['jobName'].errors, ['This field is required.'])
		self.assertEqual(response.context['jobsForm']['jobDescription'].errors, ['This field is required.'])
		self.assertEqual(response.context['jobsForm']['startDate'].errors, ['This field is required.'])
		self.assertEqual(response.context['jobsForm']['endDate'].errors, ['This field is required.'])
	
	def test_duplicate_job_in_same_event(self):
		event = Event.objects.create(eventName='test_event', noOfVolunteersRequired=10, startDate='2014-05-05 05:05:05', endDate='2014-05-05 05:05:05')
		Job.objects.create(event=Event.objects.get(eventName='test_event'), jobName='test_jobName',
				jobDescription='test_jobDescription_1', noOfVolunteersRequired=10, startDate='2014-05-05 05:05:05',
				endDate='2014-05-05 05:05:05')

		self.assertEqual(1, Event.objects.filter(eventName='test_event').count())
		self.assertEqual(1, Job.objects.filter(event__eventName='test_event',jobName='test_jobName').count())

		c = Client()
		user = User.objects.create_user(first_name='Jayesh',last_name='Lahori',email='jlahori92@gmail.com',username='jlahori',password='password')
		profile = AdminProfile.objects.create(user=user,address='IIIT-H',location='Hyderabad',state='Andhra Pradesh',
				organization=Organization.objects.create(name='LinkedIn', location='blr'),phone='9581845730')

		self.assertEqual(1, AdminProfile.objects.filter(user__username='jlahori').count())
		c.login(username='jlahori', password='password')

		response = c.post('/AdminUnit/job/',{'event' : event.id, 'jobName' : 'test_jobName',
			'jobDescription' : 'test_jobDescription_2', 'startDate' : '2014-05-05 05:05:05',
			'endDate' : '2014-05-05 05:05:05', 'noOfVolunteersRequired' : 5})

		self.assertEqual(200, response.status_code)
		self.assertEqual(len(response.context['jobsForm'].non_field_errors()), 1)
		self.assertEqual(response.context['jobsForm'].non_field_errors()[0], "Job with this Event and JobName already exists.")
