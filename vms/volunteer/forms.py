from django import forms
from django.db import models
from django.forms import ModelForm
from volunteer.models import Volunteer

class ReportForm(forms.Form):
    event_name = forms.RegexField(regex=r'^[(A-Z)|(a-z)|(0-9)|(\s)|(\.)|(,)|(\-)|(!)]+$', max_length=75, required=False)
    job_name = forms.RegexField(regex=r'^[(A-Z)|(a-z)|(\s)]+$', max_length=75, required=False)
    date = forms.DateField(required=False)

class SearchVolunteerForm(forms.Form):
    first_name = forms.RegexField(regex=r'^[(A-Z)|(a-z)|(\s)|(\-)]+$', max_length=30, required=False)
    last_name = forms.RegexField(regex=r'^[(A-Z)|(a-z)|(\s)|(\-)]+$', max_length=30, required=False)
    city = forms.RegexField(regex=r'^[(A-Z)|(a-z)|(\s)|(\-)]+$', max_length=75, required=False)
    state = forms.RegexField(regex=r'^[(A-Z)|(a-z)|(\s)|(\-)]+$', max_length=75, required=False)
    country = forms.RegexField(regex=r'^[(A-Z)|(a-z)|(\s)|(\-)]+$', max_length=75, required=False)
    organization = forms.RegexField(regex=r'^[(A-Z)|(a-z)|(\s)|(\-)]+$', max_length=75, required=False)
    
class VolunteerForm(ModelForm):
    class Meta:
        model = Volunteer
        fields = ['first_name', 'last_name', 'address', 'city', 'state', 'country', 'phone_number', 'unlisted_organization', 'email', 'websites', 'description', 'resume', 'resume_file']
