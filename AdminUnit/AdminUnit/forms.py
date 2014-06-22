from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Event, AssignedJob
from django.forms import ModelForm

class UserForm(forms.Form):
	'''
	As per the models, Registering a user involves two forms, user from auth models and custom-defines userprofile. This class is associated with forms for user table
	from auth.
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


class UserProfileForm(forms.Form):
	'''
	As per the models, Registering a user involves two forms, user from auth models and custom-defined userProfile. This class is associated with forms for userProfile
	table.
	'''
	address = forms.CharField(required=True)
	location = forms.CharField(required=True)
	state = forms.CharField(required=True)
	organization = forms.CharField(required=True)
	phone = forms.CharField(required=True)

	# Check if both passwords are same
  	def clean_phone(self):
     		phone = self.cleaned_data['phone']
     		if len(phone)!=10:
       			raise forms.ValidationError("Invalid phone number.")
		for i in range(10):
			if phone[i].isalpha():
       				raise forms.ValidationError("Invalid phone number.")
     		return phone


class EventForm(ModelForm):
	'''
	Class Responsible for displaying forms of Event Class, inheriting ModelForm Class.
	'''
	class Meta:
     		model = Event
  
  	# To ensure noOfVolunteersRequired > 0
  	def clean_noOfVolunteersRequired(self):
      		noOfVolunteersRequired = self.cleaned_data['noOfVolunteersRequired']
      		print noOfVolunteersRequired
      		if noOfVolunteersRequired <= 0:
        		raise forms.ValidationError("Please input atleast one volunteer")
      		return noOfVolunteersRequired

	# Check if this username is not already existing
 	def clean_eventName(self):
 		eventName = self.cleaned_data['eventName']
     		try:
        		Event.objects.get(eventName=eventName)
     		except Event.DoesNotExist:
			return username
 		raise forms.ValidationError('Event Name "%s" is already in use.' % eventName)


class AssignJobsForm(ModelForm):
	'''
	Class Responsible for displaying forms of AssignedJob Class, inheriting ModelForm Class.
	'''
	class Meta:
		model = AssignedJob
