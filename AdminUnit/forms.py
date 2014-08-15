from django import forms
from django.contrib.auth.models import User
from AdminUnit.models import *
from django.forms import ModelForm, TextInput
from django.contrib.admin import widgets


class UserForm(forms.Form):
    """
    This class creates a form instance as per the Django auth table
    This is used alongwith AdminProfile/VolunteerProfile for for
    registering users
    """
    firstname = forms.CharField(required=True)
    lastname = forms.CharField(required=True)
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm password",
        required=True)

    # Check if both passwords are same
    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    # Check if this username is not already existing
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            'Username "%s" is already in use.' %
            username)


class AdminProfileForm(ModelForm):
    """
    ModelForm for AdminProfile Class
    Used for registering admins into the system
    """
    class Meta:
        model = AdminProfile
        fields = ['address', 'location', 'state', 'organization', 'phone']


class VolunteerProfileForm(ModelForm):
    """
    ModelForm for AdminProfile Class
    Used for registering admins into the system
    Will be replaced by Irish's instance
    """
    class Meta:
        model = VolunteerProfile
        fields = ['address', 'location', 'state', 'organization', 'phone']


class EventForm(ModelForm):
    """
    ModelForm for Event Class
    Used by admins to create Events
    """
    class Meta:
        model = Event
        fields = ['eventName', 'startDate', 'endDate']
        widgets = {
            'startDate': TextInput(
                attrs={
                    'placeholder': 'YYYY-MM-DD HH:MM:SS'}),
            'endDate': TextInput(
                attrs={
                    'placeholder': 'YYYY-MM-DD HH:MM:SS'}),
        }


class JobsForm(ModelForm):
    """
    ModelForm for Jobs Class
    Used by admins to create Jobs inside events
    """
    class Meta:
        model = Job
        widgets = {
            'startDate': TextInput(
                attrs={
                    'placeholder': 'YYYY-MM-DD HH:MM:SS'}),
            'endDate': TextInput(
                attrs={
                    'placeholder': 'YYYY-MM-DD HH:MM:SS'}),
        }
        fields = ['event', 'jobName', 'jobDescription', 'startDate', 'endDate']


class OrgForm(ModelForm):
    """
    ModelForm for Organization Class
    """
    class Meta:
        model = Organization
        fields = ['name', 'location']


class ShiftForm(ModelForm):
    """
    ModelForm for Shift class
    """
    class Meta:
        model = Shift
        widgets = {
            'startTime': TextInput(
                attrs={
                    'placeholder': 'YYYY-MM-DD HH:MM:SS'}),
            'endTime': TextInput(
                attrs={
                    'placeholder': 'YYYY-MM-DD HH:MM:SS'}),
        }


class SATForm(ModelForm):
    """
    ModelForm for SAT class
    """
    class Meta:
        model = SAT
        fields = ['shift', 'volunteer']


class WLTAdminForm(ModelForm):
    """
    ModelForm for WLT class
    This will be used to display WLT forms to Admin
    """
    class Meta:
        model = WLT
        fields = ['shift', 'volunteer', 'startTime', 'endTime']
        widgets = {
            'startTime': TextInput(
                attrs={
                    'placeholder': 'YYYY-MM-DD HH:MM:SS'}),
            'endTime': TextInput(
                attrs={
                    'placeholder': 'YYYY-MM-DD HH:MM:SS'}),
        }


class WLTVolunteerForm(ModelForm):
    """
    ModelForm for WLT class
    This will be used to display WLT forms to Volunteer
    """
    class Meta:
        model = WLT
        fields = ['shift', 'startTime', 'endTime']
        widgets = {
            'startTime': TextInput(
                attrs={
                    'placeholder': 'YYYY-MM-DD HH:MM:SS'}),
            'endTime': TextInput(
                attrs={
                    'placeholder': 'YYYY-MM-DD HH:MM:SS'}),
        }


class SelectEventForm(ModelForm):

    class Meta:
        model = AllEvents


class SelectOrgForm(ModelForm):

    class Meta:
        model = AllOrgs


class SelectTimeForm(forms.Form):
    startTime = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'YYYY-MM-DD HH:MM:SS'}))
    endTime = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'YYYY-MM-DD HH:MM:SS'}))


class SelectHoursForm(forms.Form):
    fromHours = forms.IntegerField()
    toHours = forms.IntegerField()
