from django.core.validators import RegexValidator
from django.db import models
from volunteer.models import Volunteer

class Job(models.Model):
    job_title = models.CharField(max_length=45)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField()

class VolunteerJob(models.Model):
    volunteer = models.ForeignKey(Volunteer)
    job = models.ForeignKey(Job)
    hours_worked = models.FloatField()
