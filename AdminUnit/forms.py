from django import forms
from django.contrib.auth.models import User
from AdminUnit.models import *
from django.forms import ModelForm

class UserForm(forms.Form):
	'''
	As per the models, Registering a user involves two forms, user from auth models and custom-defines userprofile. This class is associated with forms for user table from auth.
	'''
	firstname = forms.CharField(required=True)
	lastname = forms.CharField(required=True)
	username = forms.CharField(required=True)
	email = forms.EmailField(required=True)
	password = forms.CharField(widget=forms.PasswordInput,required=True)
	password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm password", required=True)

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
 		raise forms.ValidationError('Username "%s" is already in use.' % username)

class UserProfileForm(ModelForm):
	'''
	As per the models, Registering a user involves two forms, user from auth models and custom-defined userProfile. This class is associated with forms for userProfile table.
	'''
	class Meta:
		model = UserProfile
		fields = ['address','location','state','organization','phone']

class EventForm(ModelForm):
	'''
	Class Responsible for displaying forms of Event Class, inheriting ModelForm Class.
	'''
	class Meta:
     		model = Event

class JobsForm(ModelForm):
	'''
	Class Responsible for displaying forms of AssignedJob Class, inheriting ModelForm Class.
	'''
	class Meta:
		model = Job

class OrgForm(ModelForm):
	'''
	Class Responsible for displaying forms of AssignedJob Class, inheriting ModelForm Class.
	'''
	class Meta:
		model = Organization
		fields = ['name','location']

class ShiftForm(ModelForm):
	'''
	Class for creating forms to insert/edit data into Shifts Model
	'''
	class Meta:
		model = Shift

class SelectEventForm(ModelForm):
	class Meta:
		model = AllEvents

class SelectOrgForm(ModelForm):
	class Meta:
		model = AllOrgs

class SelectTimeForm(forms.Form):
	startTime = forms.DateTimeField()
	endTime = forms.DateTimeField()

class SelectHoursForm(forms.Form):
	fromHours = forms.IntegerField()
	toHours = forms.IntegerField()
