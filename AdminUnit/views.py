from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.db.models import Q

#from .forms import UserForm, UserProfileForm, EventForm, JobsForm, OrgForm
#from .models import UserProfile, Event, Job, Organization

from AdminUnit.forms import *
from AdminUnit.models import *

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
			orgObject=Organization.objects.get(Q(name=userProfileForm.cleaned_data['organization']))
			orgObject.noOfVolunteers += 1
			orgObject.save()
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
def job(request,jobId=None):
	'''
	Controller to Edit/Create Jobs. In case of Creating new job, jobId is None and therefore jobInstance
	'''
	if jobId:
    		jobInstance = Job.objects.get(pk=jobId)
  	else:
    		jobInstance = None

	# POST Request, submitted form has come as a request. If jobInstance is none implies new record has to be saved else edited record
  	if request.method == 'POST':
     		jobsForm = JobsForm(request.POST, instance = jobInstance)
     		if jobsForm.is_valid():
			newRecord = jobsForm.save();
			return HttpResponse('Job Created')
  	else:
     		jobsForm = JobsForm(instance = jobInstance)
  	
	return render(request, "AdminUnit/jobs.html",{"jobsForm" : jobsForm})

@login_required
def allEvents(request):
	'''
	Controller responsible for displaying all Events that have been registered, alongside will be displayed the links to edit/delete an event
	'''
  	allEvents = Event.objects.all()
  	return render(request, "AdminUnit/all_events.html", {"allEvents" : allEvents});

@login_required
def allJobs(request):
	'''
	Controller responsible for displaying jobs registered across all Events that have been registered, alongside will be displayed the links to edit/delete the same
	'''
  	allJobs = Job.objects.all()
  	return render(request, "AdminUnit/all_jobs.html", {"allJobs" : allJobs});

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
  	Job.objects.filter(pk=jobId).delete()
  	allJobs = Job.objects.all()
  	return render(request, "AdminUnit/all_jobs.html", {"allJobs" : allJobs});

@login_required
def editOrg(request, orgId=None):
	'''
	Use to Edit/Create Organization, In case of Creating new Org orgId is None and therefore orgInstance
	'''
	if orgId:
		orgInstance = Organization.objects.get(pk=orgId)
 	else:
		orgInstance = None

	# POST Request, submitted form has come as a request. If eventInstance is none implies new record has to be saved else edited record
  	if request.method == 'POST':
   		 orgForm = OrgForm(request.POST,instance = orgInstance)
		 if orgForm.is_valid():
      			newRecord = orgForm.save()
      			return HttpResponse("Org Created/Edited")
  	
	# to handle a GET Request
	else:
    		orgForm = OrgForm(instance=orgInstance)
  	
	return render(request, "AdminUnit/org.html",{"orgForm" : orgForm})

@login_required
def allOrgs(request):
	'''
	Controller responsible for displaying all Events that have been registered, alongside will be displayed the links to edit/delete an event
	'''
  	allOrgs = Organization.objects.all()
  	return render(request, "AdminUnit/all_orgs.html", {"allOrgs" : allOrgs});

@login_required
def deleteOrg(request,orgId=None):
	'''
	Delete's a job with a given primary key
	'''
  	Organization.objects.filter(pk=orgId).delete()
  	allOrgs = Organization.objects.all()
  	return render(request, "AdminUnit/all_orgs.html", {"allOrgs" : allOrgs});

@login_required
def searchByEvent(request):
	if request.method == 'POST':
		selectEventForm = SelectEventForm(request.POST)
		if selectEventForm.is_valid():
			eventName = selectEventForm.cleaned_data['event']
			jobs = Job.objects.filter(event__eventName=eventName)
			selectEventForm = {}
			return render(request, "AdminUnit/search_by_events.html", {"jobs" : jobs, "selectEventForm" : selectEventForm});
	else:
		selectEventForm = SelectEventForm()
		jobs = {}
		return render(request, "AdminUnit/search_by_events.html", {"jobs" : jobs, "selectEventForm" : selectEventForm});

@login_required
def searchByTime(request):
	if request.method == 'POST':
		selectTimeForm = SelectTimeForm(request.POST)
		if selectTimeForm.is_valid():
			startTime = selectTimeForm.cleaned_data['startTime']
			endTime = selectTimeForm.cleaned_data['endTime']
			print str(startTime) + ' ' + str(endTime)
			jobs = Job.objects.filter(startDate__gte=startTime,endDate__lte=endTime)
			selectTimeForm = {}
			return render(request, "AdminUnit/search_by_time.html", {"jobs" : jobs, "selectTimeForm" : selectTimeForm});
	else:
		selectTimeForm = SelectTimeForm()
		jobs = {}
		return render(request, "AdminUnit/search_by_time.html", {"jobs" : jobs, "selectTimeForm" : selectTimeForm});

@login_required
def searchEmployeeByOrg(request):
	if request.method == 'POST':
		selectOrgForm = SelectOrgForm(request.POST)
		if selectOrgForm.is_valid():
			orgName = selectOrgForm.cleaned_data['org']
			users = UserProfile.objects.filter(organization__name=orgName)
			selectOrgForm = {}
			return render(request, "AdminUnit/search_by_org.html", {"users" : users, "selectOrgForm" : selectOrgForm});
	else:
		selectOrgForm = SelectOrgForm()
		users = {}
		return render(request, "AdminUnit/search_by_org.html", {"users" : users, "selectOrgForm" : selectOrgForm});

@login_required
def manageShift(request, shiftId=None):
	'''
	Use to Edit/Create Shifts, In case of Creating new Org orgId is None and therefore orgInstance
	'''
	if shiftId:
		shiftInstance = Shift.objects.get(pk=shiftId)
 	else:
		shiftInstance = None

	# POST Request, submitted form has come as a request. If eventInstance is none implies new record has to be saved else edited record
  	if request.method == 'POST':
   		 shiftForm = ShiftForm(request.POST,instance = shiftInstance)
		 if shiftForm.is_valid():
      			newRecord = shiftForm.save()
      			return HttpResponse("Shift Created/Edited")
  	
	# to handle a GET Request
	else:
    		shiftForm = ShiftForm(instance=shiftInstance)

	return render(request, "AdminUnit/shift.html", {"shiftForm" : shiftForm})

@login_required
def allShifts(request):
	'''
	Controller responsible for displaying all Events that have been registered, alongside will be displayed the links to edit/delete an event
	'''
  	allShifts = Shift.objects.all()
  	return render(request, "AdminUnit/all_shifts.html", {"allShifts" : allShifts});

@login_required
def deleteShift(request,shiftId=None):
	'''
	Delete's a job with a given primary key
	'''
  	Shift.objects.filter(pk=shiftId).delete()
  	allShifts = Shift.objects.all()
  	return render(request, "AdminUnit/all_shifts.html", {"allShifts" : allShifts});

@login_required
def createShift(request, jobId=None, eventId=None, userName=None):
      	shift = Shift(event=Event.objects.get(pk=eventId),job=Job.objects.get(pk=jobId),volunteer=UserProfile.objects.get(user__username=userName),hours=1)
	shift.save()
	return HttpResponse("Shift Created");

@login_required
def reportHoursByOrg(request):
	if request.method == 'POST':
		selectHoursForm = SelectHoursForm(request.POST)
		if selectHoursForm.is_valid():
			fromHours = selectHoursForm.cleaned_data['fromHours']
			toHours = selectHoursForm.cleaned_data['toHours']
			shifts = Shift.objects.all()
			counts = {}
			for shift in shifts:
				org = shift.volunteer.organization.name
				if org in counts:
					counts[org]+=shift.hours
				else:
					counts[org]=shift.hours
			data = []
			for org in counts:
				if counts[org] >= fromHours and counts[org] <= toHours:
					data.append([org,counts[org]])
			return render(request, "AdminUnit/report_hours_by_org.html", {"values" : data, "selectHoursForm" : {}})
	else:
		selectHoursForm = SelectHoursForm()
		return render(request, "AdminUnit/report_hours_by_org.html", {"values" : {}, "selectHoursForm" : selectHoursForm})

@login_required
def reportVolunteersByOrg(request):
	users = UserProfile.objects.all()
	counts = {}
	for user in users:
		org = user.organization.name
		if org in counts:
			counts[org]+=1
		else:
			counts[org]=1
	data = []
	for org in counts:
		data.append([org,counts[org]])
	values = { 'values' : data }
	return render(request, "AdminUnit/report_volunteers_by_org.html", values)

@login_required
def reportHoursByEvent(request):
	if request.method == 'POST':
		selectEventForm = SelectEventForm(request.POST)
		if selectEventForm.is_valid():
			eventName = selectEventForm.cleaned_data['event']
			shifts = Shift.objects.filter(event__eventName=eventName)
			counts = {}
	
			for shift in shifts:
				org = shift.volunteer.organization.name
				if org in counts:
					counts[org]+=shift.hours
				else:
					counts[org]=shift.hours
		
			data = []
			for org in counts:
				data.append([org,counts[org]])
			selectEventForm = {}
			return render(request, "AdminUnit/report_hours_by_event.html", {"values" : data, "selectEventForm" : selectEventForm})
	else:
		selectEventForm = SelectEventForm()
		data = []
		return render(request, "AdminUnit/report_hours_by_event.html", {"values" : data, "selectEventForm" : selectEventForm})

@login_required
def reportHoursByTime(request):
	if request.method == 'POST':
		selectTimeForm = SelectTimeForm(request.POST)
		if selectTimeForm.is_valid():
			startTime = selectTimeForm.cleaned_data['startTime']
			endTime = selectTimeForm.cleaned_data['endTime']
			shifts = Shift.objects.filter(event__startDate__gte=startTime,event__endDate__lte=endTime)
			counts = {}
	
			for shift in shifts:
				org = shift.volunteer.organization.name
				if org in counts:
					counts[org]+=shift.hours
				else:
					counts[org]=shift.hours
		
			data = []
			for org in counts:
				data.append([org,counts[org]])
			selectTimeForm = {}
			return render(request, "AdminUnit/report_hours_by_time.html", {"values" : data, "selectTimeForm" : selectTimeForm})
	else:
		selectTimeForm = SelectTimeForm()
		data = []
		return render(request, "AdminUnit/report_hours_by_time.html", {"values" : data, "selectTimeForm" : selectTimeForm})
