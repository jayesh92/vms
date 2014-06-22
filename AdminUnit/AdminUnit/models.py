from django.db import models
from django.contrib.auth.models import User
from django.db.models import ForeignKey
from django import forms
import datetime

class UserProfile(models.Model):
	'''
	Model for UserProfile, each record is a one-to-one mapping ro user model from auth and also contains few other parameters
	'''
    	user = models.OneToOneField(User)

    	address = models.CharField(max_length=128)
    	location = models.CharField(max_length=128)
    	state = models.CharField(max_length=128)
    	organization =  models.CharField(max_length=128)
    	phone = models.CharField(max_length=128)

    	def __unicode__(self):
		return self.user.username


class Event(models.Model):
	'''
	Model structure of Event Table
	'''
	eventName = models.CharField(max_length=128)
    	noOfVolunteersRequired = models.IntegerField()
    	startDate = models.DateTimeField()
    	endDate = models.DateTimeField()

    	def __unicode__(self):
		return self.eventName


class AssignedJob(models.Model):
	'''
	Model structure for Jobs, each job has a many-to-one relationship with events, i.e., there can be 'n' number of jobs associated with one single event. 'event' is
	therefore a foreign key
	'''
	event = models.ForeignKey(Event)

	volunteerName = models.CharField(max_length=128)
	job = models.CharField(max_length=128)

	def __unicode__(self):
		return self.event.eventName
