from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response

from .forms import UserForm, UserProfileForm, EventForm, AssignJobsForm
from .models import UserProfile, Event, AssignedJob

def index(request):
	'''
	Controller for VMS Homepage
	'''
	return render(request,"AdminUnit/index.html")

def register(request):
	'''
	This method is used to register new user into the system as a volunteer
	'''
	
	# POST Request, submitted form has come as a request
  	if request.method == 'POST':
    		userForm = UserForm(request.POST)
    		userProfileForm = UserProfileForm(request.POST)

    		if userForm.is_valid() and userProfileForm.is_valid():
      			user = User.objects.create_user(first_name=userForm.cleaned_data['firstname'],last_name=userForm.cleaned_data['lastname'],
					  		email=userForm.cleaned_data['email'],username=userForm.cleaned_data['username'],
							password=userForm.cleaned_data['password'])

      			userProfile = UserProfile(user=user, address=userProfileForm.cleaned_data['address'],location=userProfileForm.cleaned_data['location'],
        					 state=userProfileForm.cleaned_data['state'],organization=userProfileForm.cleaned_data['organization'],
						 phone=userProfileForm.cleaned_data['phone'])

      			userProfile.save()
      			return HttpResponse("You have registered, login available @ AdminUnit/")

  	# GET Request, render empty form
  	else:
  		 userForm = UserForm()
  		 userProfileForm = UserProfileForm()
 
  	return render(request, "AdminUnit/register.html",{ "userForm" : userForm , "userProfileForm" : userProfileForm })

def login_process(request):
	'''
	Authenticate a user against their credentials
	'''

	# POST Request, submitted form has come as a request, authenticate and redirect to apt page
  	if request.method == 'POST':
      		username = request.POST['username']
      		password = request.POST['password']

      		user = authenticate(username=username, password=password)

      		if user:
          		if user.is_active:
        	      		login(request,user)
        	      		return HttpResponse("You are logged in, logout available @ AdminUnit/")
        	  	else:
              			return HttpResponse("Your account is disabled.")
      		else:
          		return HttpResponse("Invalid login details supplied.")

  	# GET Request, display login form template
  	else:
        	return render(request,'AdminUnit/login.html')

@login_required
def logout_process(request):
	'''
	logout a user
	'''
    	logout(request)
    	return HttpResponseRedirect('/AdminUnit/')

@login_required
def editEvent(request, eventId=None):
	'''
	Use to Edit/Create Event, In case of Creating new event eventId is None and therefore eventInstance
	'''
	if eventId:
		eventInstance = Event.objects.get(pk=eventId)
 	else:
		eventInstance = None

	# POST Request, submitted form has come as a request. If eventInstance is none implies new record has to be saved else edited record
  	if request.method == 'POST':
   		 eventForm = EventForm(request.POST,instance = eventInstance)
		 if eventForm.is_valid():
      			newRecord = eventForm.save()
      			return HttpResponse("Event Created/Edited")
  	
	# to handle a GET Request
	else:
    		eventForm = EventForm(instance=eventInstance)
  	
	return render(request, "AdminUnit/event.html",{"eventForm" : eventForm})

@login_required
def assignJob(request,jobId=None):
	'''
	Controller to Edit/Create Jobs. In case of Creating new job, jobId is None and therefore jobInstance
	'''
	if jobId:
    		jobInstance = AssignedJob.objects.get(pk=jobId)
  	else:
    		jobInstance = None

	# POST Request, submitted form has come as a request. If jobInstance is none implies new record has to be saved else edited record
  	if request.method == 'POST':
     		assignJobsForm = AssignJobsForm(request.POST, instance = jobInstance)
     		if assignJobsForm.is_valid():
			newRecord = assignJobsForm.save();
			return HttpResponse('Job Assigned')
  	else:
     		assignJobsForm = AssignJobsForm(instance = jobInstance)
  	
	return render(request, "AdminUnit/assign_jobs.html",{"assignJobsForm" : assignJobsForm})

@login_required
def allEvents(request):
	'''
	Controller responsible for displaying all Events that have been registered, alongside will be displayed the links to edit/delete an event
	'''
  	allEvents = Event.objects.all()
  	return render(request, "AdminUnit/all_events.html", {"allEvents" : allEvents});

@login_required
def allAssignedJobs(request):
	'''
	Controller responsible for displaying jobs registered across all Events that have been registered, alongside will be displayed the links to edit/delete the same
	'''
  	allAssignedJobs = AssignedJob.objects.all()
  	return render(request, "AdminUnit/all_assigned_jobs.html", {"allAssignedJobs" : allAssignedJobs});

@login_required
def deleteEvent(request,eventId=None):
	'''
	Delete's an event with a given primary key
	'''
  	Event.objects.filter(pk=eventId).delete()
  	allEvents = Event.objects.all()
  	return render(request, "AdminUnit/all_events.html", {"allEvents" : allEvents});

@login_required
def deleteJob(request,jobId=None):
	'''
	Delete's a job with a given primary key
	'''
  	AssignedJob.objects.filter(pk=jobId).delete()
  	allAssignedJobs = AssignedJob.objects.all()
  	return render(request, "AdminUnit/all_assigned_jobs.html", {"allAssignedJobs" : allAssignedJobs});

