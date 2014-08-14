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


class AdminProfile(models.Model):
    """
    Model for AdminProfile,
    Each record is a one-to-one mapping to `user model` from
    auth and also contains few other parameters
    """
    user = models.OneToOneField(User)

    address = models.CharField(
        max_length=128,
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
                r'^(\d{10})$',
            )
        ]
    )

    def __unicode__(self):
        return self.user.username


class VolunteerProfile(models.Model):
    """
    Model for VolunteerProfile, Will be replaced by Irish` volunteer model
    Each record is a one-to-one mapping to `user model` from
    auth and also contains few other parameters
    """
    user = models.OneToOneField(User)

    address = models.CharField(
        max_length=128,
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
                r'^(\d{10})$',
            )
        ]
    )

    def __unicode__(self):
        return self.user.username


class Event(models.Model):
    eventName = models.CharField(max_length=128, unique=True)
    noOfVolunteersAssigned = models.IntegerField(
        default=0,
        validators=[
            RegexValidator(
                r'^[0-9]*',
            )
        ]
    )
    noOfVolunteersWorked = models.IntegerField(
        default=0,
        validators=[
            RegexValidator(
                r'^[0-9]*',
            )
        ]
    )
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()

    def __unicode__(self):
        return self.eventName


class Job(models.Model):
    """
    Model structure for Jobs,
    Each job is associated with some event, therefore has a
    Foreign Key relationship with event table
    """
    event = models.ForeignKey(Event)

    jobName = models.CharField(max_length=128)
    jobDescription = models.CharField(max_length=256)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    noOfVolunteersAssigned = models.IntegerField(
        default=0,
        validators=[
            RegexValidator(
                r'^[0-9]*',
            )
        ]
    )
    noOfVolunteersWorked = models.IntegerField(
        default=0,
        validators=[
            RegexValidator(
                r'^[0-9]*',
            )
        ]
    )

    class Meta:
        unique_together = (('event', 'jobName'))

    def __unicode__(self):
        return self.jobName


class Shift(models.Model):
    """
    Model structure for Shifts,
    Each shift is store for records of the forms
    <event, volunteer, job, hours>
    """
    event = models.ForeignKey(Event)
    job = models.ForeignKey(Job)
    location = models.CharField(max_length=128)
    how = models.CharField(max_length=128)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()

    class Meta:
        unique_together = (('event', 'job', 'startTime', 'endTime'))

    def __unicode__(self):
        return self.event.eventName + '_' + self.job.jobName + '_' + str(self.startTime) + '_' + str(self.endTime)


class SAT(models.Model):
    """
    Assigned hours by Admin
    """
    shift = models.ForeignKey(Shift)
    volunteer = models.ForeignKey(VolunteerProfile)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    hours = models.FloatField(default=0)

    class Meta:
        unique_together = (('shift', 'volunteer'))


class WLT(models.Model):
    """
    Actual Work looged by Volunteers
    """
    shift = models.ForeignKey(Shift)
    volunteer = models.ForeignKey(VolunteerProfile)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    hours = models.FloatField(default=0)

    class Meta:
        unique_together = (('shift', 'volunteer'))


class AllEvents(models.Model):
    event = models.ForeignKey(Event, blank=False)


class AllOrgs(models.Model):
    org = models.ForeignKey(Organization)
