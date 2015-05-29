from django import forms
from django.db import models
from django.forms import ModelForm
from job.models import Job

class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = ['name', 'start_date', 'end_date', 'description']
        
    def clean(self):

        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date > end_date:
                msg = u"Start date must be before the end date"
                self._errors['start_date'] = self.error_class([msg])

        return self.cleaned_data
