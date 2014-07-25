from django.test import TestCase

from django.contrib.auth.models import User
from models import *
from django.db import IntegrityError

class TestOrganization(TestCase):
	def setUp(self):
		Organization.objects.create(
			name='LinkedIn123',
			location='Bangalore'
		)

	def test_insertion(self):
		self.assertEqual(1,len(Organization.objects.filter(name='LinkedIn')))

	def test_duplication(self):
		self.assertRaises(IntegrityError,lambda: Organization.objects.create(name='LinkedIn',location='Bangalore'))


class TestUsers(TestCase):
	def setUp(self):
		Organization.objects.create(name='LinkedIn',location='Bangalore')
		user = User.objects.create_user(first_name='Jayesh',last_name='Lahori',email='jlahori92@gmail.com',username='jlahori',password='password')
		UserProfile.objects.create(user=user,address='IIIT-H',location='Hyderabad',state='Andhra Pradesh',organization=Organization.objects.get(name='LinkedIn'),phone='9581845730')

	def test_insertion(self):
		self.assertEqual(1,len(UserProfile.objects.filter(user__username='jlahori')))

	def test_duplication(self):
		self.assertRaises(IntegrityError, lambda:  UserProfile.objects.create(user=User.objects.create_user(first_name='Jayesh',last_name='Lahori',email='jlahori92@gmail.com',username='jlahori',password='password'),address='IIIT-H',location='Hyderabad',state='Andhra Pradesh',organization=Organization.objects.get(name='LinkedIn'),phone='9581845730'))

	def test_location(self):
		UserProfile.objects.get(user__username='jlahori').delete()
		User.objects.get(username='jlahori').delete()
		self.assertEqual(0,len(UserProfile.objects.filter(user__username='jlahori')))
		self.assertEqual(0,len(User.objects.filter(username='jlahori')))
		UserProfile.objects.create(user=User.objects.create_user(first_name='Jayesh',last_name='Lahori',email='jlahori92@gmail.com',username='jlahori',password='password'),address='IIIT-H',location='Hyderabad123',state='Andhra Pradesh 132',organization=Organization.objects.get(name='LinkedIn'),phone='9581845730')
