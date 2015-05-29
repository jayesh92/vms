from django import forms
from django.db import models
from django.forms import ModelForm
from organization.models import Organization

class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = ['name']
