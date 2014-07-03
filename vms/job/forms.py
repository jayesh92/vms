from django import forms
from django.db import models
from django.forms import ModelForm
from job.models import Job, Shift

class HoursForm(forms.Form):
    start_time = forms.TimeField()
    end_time = forms.TimeField()

class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = ['job_title', 'start_date', 'end_date', 'description']

class ShiftForm(ModelForm):
    class Meta:
        model = Shift
        fields = ['date', 'location', 'start_time', 'end_time', 'max_volunteers']        
