from django.test import TestCase

from django.contrib.auth.models import User
from models import *
from django.db import IntegrityError
from django.core.exceptions import ValidationError

class TestOrganization(TestCase):
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


class TestUsers(TestCase):
	def setUp(self):
		Organization.objects.create(name='LinkedIn',location='Bangalore')
		user = User.objects.create_user(first_name='Jayesh',last_name='Lahori',email='jlahori92@gmail.com',username='jlahori',password='password')
		UserProfile.objects.create(user=user,address='IIIT-H',location='Hyderabad',state='Andhra Pradesh',organization=Organization.objects.get(name='LinkedIn'),phone='9581845730')

	def test_insertion(self):
		self.assertEqual(1,UserProfile.objects.filter(user__username='jlahori').count())

	def test_duplication(self):
		self.assertRaises(IntegrityError, lambda:  UserProfile.objects.create(user=User.objects.get(username='jlahori'),address='IIIT-H',location='Hyderabad',state='Andhra Pradesh',organization=Organization.objects.get(name='LinkedIn'),phone='9581845730'))

	def test_location(self):
		# To test if city(location) name does not allow numbers or special characters
		profile = UserProfile(user=User.objects.create_user(first_name='Jayesh',last_name='Lahori',email='jlahori92@gmail.com',username='jlahori_test2',password='password'),address='IIIT-H',location='Hyderabad123!@#',state='Andhra Pradesh',organization=Organization.objects.get(name='LinkedIn'),phone='9581845730')
		with self.assertRaises(ValidationError):
			if profile.full_clean():
				profile.save()
		self.assertEqual(0,UserProfile.objects.filter(user__username='jlahori_test2').count())

	def test_state(self):
		# To test if state does not allow numbers or special characters
		profile = UserProfile(user=User.objects.create_user(first_name='Jayesh',last_name='Lahori',email='jlahori92@gmail.com',username='jlahori_test2',password='password'),address='IIIT-H',location='Hyderabad',state='Andhra Pradesh 123 !@#',organization=Organization.objects.get(name='LinkedIn'),phone='9581845730')
		with self.assertRaises(ValidationError):
			if profile.full_clean():
				profile.save()
		self.assertEqual(0,UserProfile.objects.filter(user__username='jlahori_test2').count())


	def test_phone(self):
		# To test if phone numbers does not allow anything except 10 numbers
		profile = UserProfile(user=User.objects.create_user(first_name='Jayesh',last_name='Lahori',email='jlahori92@gmail.com',username='jlahori_test2',password='password'),address='IIIT-H',location='Hyderabad',state='Andhra Pradesh',organization=Organization.objects.get(name='LinkedIn'),phone='919581845730')
		with self.assertRaises(ValidationError):
			if profile.full_clean():
				profile.save()
		self.assertEqual(0,UserProfile.objects.filter(user__username='jlahori_test2').count())
	
	def test_organization_foreign_key(self):
		# To test only registered organizations should be allowed as valid entries
		org=Organization(name='Google',location='Hyderabad')
		profile = UserProfile(user=User.objects.create_user(first_name='Jayesh',last_name='Lahori',email='jlahori92@gmail.com',username='jlahori_test2',password='password'),address='IIIT-H',location='Hyderabad',state='Andhra Pradesh',organization=org,phone='9581845730')
		with self.assertRaises(ValidationError):
			if profile.full_clean():
				profile.save()
		self.assertEqual(0,UserProfile.objects.filter(user__username='jlahori_test2').count())

class TestEvent(TestCase):
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

class testJob(TestCase):
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

class testShift(TestCase):
	def setUp(self):
		event = Event.objects.create(eventName='event1',noOfVolunteersRequired=5,startDate='2015-05-05 05:05:05',endDate='2015-05-05 05:05:05')
		user = User.objects.create_user(first_name='Jayesh',last_name='Lahori',email='jlahori92@gmail.com',username='jlahori',password='password')
		profile = UserProfile.objects.create(user=user,address='IIIT-H',location='Hyderabad',state='Andhra Pradesh',organization=Organization.objects.create(name='LinkedIn', location='blr'),phone='9581845730')
		job = Job.objects.create(event=event, jobName='Test Job Name', jobDescription='Test Job Description', noOfVolunteersRequired=5, startDate='2015-05-05 05:05:05', endDate='2015-05-05 05:05:05')
		Shift.objects.create(event=event, volunteer=profile, job=job, hours=1)
	
	def test_insertion(self):
		self.assertEqual(1,Shift.objects.filter(event__eventName='event1',volunteer__user__username='jlahori',job__event__eventName='event1').count())

	def test_event_foreign_key(self):
		# To test if only registered events are allowed in creation of shifts
		event = Event(eventName='event2',noOfVolunteersRequired=5,startDate='2015-05-05 05:05:05',endDate='2015-05-05 05:05:05')
		shift = Shift(event=event, volunteer=UserProfile.objects.get(user__username='jlahori'), job=Job.objects.get(event__eventName='event1'), hours=1)
		with self.assertRaises(ValidationError):
			if shift.full_clean():
				job.save()
		self.assertEqual(0,Shift.objects.filter(event__eventName='event2').count())

	def test_volunteer_foreign_key(self):
		# To test if only registered volunteers are allowed in creation of shifts
		previousCount = Shift.objects.filter(event__eventName='event1').count()
		profile = UserProfile(user=User(first_name='Jayesh',last_name='Lahori',email='jlahori92@gmail.com',username='jlahori_test',password='password'),address='IIIT-H',location='Hyderabad',state='Andhra Pradesh',phone='9581845730',organization=Organization(name='Google', location='hyderabad'))
		shift = Shift(event=Event.objects.get(eventName='event1'), volunteer=profile, job=Job.objects.get(event__eventName='event1'), hours=1)
		with self.assertRaises(ValidationError):
			if shift.full_clean():
				shift.save()
		self.assertEqual(previousCount, Shift.objects.filter(event__eventName='event1').count())
