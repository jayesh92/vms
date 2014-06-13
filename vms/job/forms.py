from django import forms
from django.db import models
from django.forms import ModelForm
from job.models import Job

class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = ['job_title', 'start_date', 'start_time', 'end_date', 'end_time', 'description']
