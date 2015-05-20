from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from job.models import Job
from volunteer.models import Volunteer

class Shift(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_volunteers = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5000)
        ]
    )
    #Job to Shift is a one-to-many relationship
    job = models.ForeignKey(Job)
    #VolunteerShift is the intermediary model for the many-to-many relationship between Volunteer and Shift
    volunteers = models.ManyToManyField(Volunteer, through='VolunteerShift')

class VolunteerShift(models.Model):
    #Volunteer  to VolunteerShift is a one-to-many relationship
    volunteer = models.ForeignKey(Volunteer)
    #Shift to VolunteerShift is a one-to-many relationship
    shift = models.ForeignKey(Shift)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    #assigned_by_manager = models.BooleanField()
