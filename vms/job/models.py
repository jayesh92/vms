from django.core.validators import RegexValidator
from django.db import models
from volunteer.models import Volunteer

class Job(models.Model):
    job_title = models.CharField(
        max_length=75,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(\s)]+$',
            ),
        ],
    )
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(
        blank=True,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(0-9)|(\s)|(\.)|(,)|(\-)|(!)]+$',
            ),
        ],
    )

class Shift(models.Model):
    date = models.DateField()
    location = models.CharField(
        max_length=75,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(0-9)|(\s)|(\-)]+$',
            ),
        ],
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_volunteers = models.PositiveSmallIntegerField(
        validators=[
            RegexValidator(
                r'^[0-9]+$',
            ),
        ],
    )
    slots_remaining = models.PositiveSmallIntegerField(
        validators=[
            RegexValidator(
                r'^[0-9]+$',
            ),
        ],
    )
    #Job to Shift is a one-to-many relationship
    job = models.ForeignKey(Job)
    #VolunteerShift is the intermediary model for the many-to-many relationship between Volunteer and Shift
    volunteers = models.ManyToManyField(Volunteer, through='VolunteerShift')

class VolunteerShift(models.Model):
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    #Volunteer to VolunteerShift is a one-to-many relationship
    volunteer = models.ForeignKey(Volunteer)
    #Shift to VolunteerShift is a one-to-many relationship
    shift = models.ForeignKey(Shift)
