from django.core.validators import RegexValidator
from django.db import models
from volunteer.models import Volunteer

class Job(models.Model):
    job_title = models.CharField(max_length=45)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField()
    #VolunteerJob is the intermediary model for the many-to-many relationship between Volunteer and Jobs
    volunteers = models.ManyToManyField(Volunteer, through='VolunteerJob')

#this model tells us the jobs that a volunteer is signed up for
class VolunteerJob(models.Model):
    #Volunteer to VolunteerJob is a one-to-many relationship
    volunteer = models.ForeignKey(Volunteer)
    #Job to VolunteerJob is a one-to-many relationship
    job = models.ForeignKey(Job)

#this model is for keeping track of hours worked
class JobHoursLog(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    hours_worked = models.FloatField()
    #Volunteer to JobHoursLog is a one-to-many relationship
    volunteer = models.ForeignKey(Volunteer)
    job = models.ForeignKey(Job)
