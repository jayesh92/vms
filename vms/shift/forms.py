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
        fields = ['date', 'location', 'start_time', 'end_time', 'max_volunteers']     
