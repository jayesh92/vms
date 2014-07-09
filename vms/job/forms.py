from django import forms
from django.db import models
from django.forms import ModelForm
from job.models import Job

class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = ['job_title', 'start_date', 'end_date', 'description']   
