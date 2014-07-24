from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models import ForeignKey
from django import forms
import datetime


class Organization(models.Model):
	name = models.CharField(
			max_length=128,
			unique=True,
			validators=[
				RegexValidator(
					r'^[(A-Z)|(a-z)|(\s)]+$',
				)
			]
		)
	location = models.CharField(
			max_length=128,
			validators=[
				RegexValidator(
					r'^[(A-Z)|(a-z)|(\s)]+$',
				)
			]
		)
	noOfVolunteers = models.IntegerField(default=0)

	def __unicode__(self):
		return self.name

class UserProfile(models.Model):
	'''
	Model for UserProfile, each record is a one-to-one mapping ro user model from auth and also contains few other parameters
	'''
    	user = models.OneToOneField(User)

    	address = models.CharField(
			max_length=128,
			validators=[
				RegexValidator(
					r'^[(A-Z)|(a-z)|(\s)|(0-9)]+$',
				)
			]
		)
    	location = models.CharField(
			max_length=128,
			validators=[
				RegexValidator(
					r'^[(A-Z)|(a-z)|(\s)]+$',
				)
			]
		)
    	state = models.CharField(
			max_length=128,
			validators=[
				RegexValidator(
					r'^[(A-Z)|(a-z)|(\s)]+$',
				)
			]
		)
	organization = models.ForeignKey(Organization)
    	phone = models.CharField(
			max_length=128,
			validators=[
				RegexValidator(
					r'\d{10}',
				)
			]
		)

    	def __unicode__(self):
		return self.user.username

class Event(models.Model):
	'''
	Model structure of Event Table
	'''
	eventName = models.CharField(max_length=128, unique=True)
    	noOfVolunteersRequired = models.IntegerField(
					validators=[
						RegexValidator(
							r'^[1-9][0-9]*',
						)
					]
				)
    	startDate = models.DateTimeField()
    	endDate = models.DateTimeField()

    	def __unicode__(self):
		return self.eventName

class Job(models.Model):
	'''
	Model structure for Jobs, each job has a many-to-one relationship with events, i.e., there can be 'n' number of jobs associated with one single event. 'event' is therefore a foreign key
	'''
	event = models.ForeignKey(Event)

	jobName = models.CharField(max_length=128)
	jobDescription = models.CharField(max_length=256)
    	startDate = models.DateTimeField()
    	endDate = models.DateTimeField()
    	noOfVolunteersRequired = models.IntegerField(
					validators=[
						RegexValidator(
							r'^[1-9][0-9]*',
						)
					]
				)

	def __unicode__(self):
		return self.jobName

class Shift(models.Model):
	event = models.ForeignKey(Event)
	volunteer = models.ForeignKey(UserProfile)
	job = models.ForeignKey(Job)
	hours = models.IntegerField(
			validators=[
				RegexValidator(
					r'^[1-9][0-9]*',
				)
			]
		)

class AllEvents(models.Model):
	event = models.ForeignKey(Event)

class AllOrgs(models.Model):
	org = models.ForeignKey(Organization)
