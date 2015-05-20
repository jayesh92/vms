from django import forms
from django.db import models
from django.forms import ModelForm
from shift.models import Shift

class HoursForm(forms.Form):
    start_time = forms.TimeField()
    end_time = forms.TimeField()

class ShiftForm(ModelForm):
    class Meta:
        model = Shift
        fields = ['date', 'start_time', 'end_time', 'max_volunteers']     

    #we don't check that start_time > end_time because we could 
    #start at 11pm and end at 1am and this test would fail
