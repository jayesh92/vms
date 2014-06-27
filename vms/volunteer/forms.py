from django import forms
from django.db import models
from django.forms import ModelForm
from volunteer.models import Volunteer

class SearchVolunteerForm(forms.Form):
    first_name = forms.RegexField(regex=r'^[(A-Z)|(a-z)|(\s)]+$', max_length=20, required=False)
    last_name = forms.RegexField(regex=r'^[(A-Z)|(a-z)|(\s)]+$', max_length=20, required=False)
    city = forms.RegexField(regex=r'^[(A-Z)|(a-z)|(\s)]+$', max_length=20, required=False)
    state = forms.RegexField(regex=r'^[(A-Z)|(a-z)|(\s)]+$', max_length=20, required=False)
    country = forms.RegexField(regex=r'^[(A-Z)|(a-z)|(\s)]+$', max_length=20, required=False)
    company = forms.RegexField(regex=r'^[(A-Z)|(a-z)|(\s)]+$', max_length=20, required=False)

class VolunteerForm(ModelForm):
    class Meta:
        model = Volunteer
        fields = ['first_name', 'last_name', 'address', 'city', 'state', 'country', 'phone_number', 'company', 'unlisted_organization', 'email', 'websites', 'description', 'resume', 'resume_file']
