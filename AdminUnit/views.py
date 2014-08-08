from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.core.mail import send_mail
from django.db.models import Q

from AdminUnit.forms import *
from AdminUnit.models import *

def checkAdmin(user):
	if user:
		if user.is_superuser or AdminProfile.objects.filter(user__username=user.username).count() == 1:
			return True
	return False

def checkVolunteer(user):
	if user:
		if VolunteerProfile.objects.filter(user__username=user.username).count() == 1:
			return True
	return False

def index(request):
	'''
	Controller for VMS Homepage
	'''
	if request.user:
		if checkAdmin(request.user):
			return render(request,"AdminUnit/index.html",{"admin" : True, "volunteer" : False})
		elif checkVolunteer(request.user):
			return render(request,"AdminUnit/index.html",{"admin" : False, "volunteer" : True})
	return render(request,"AdminUnit/index.html",{"admin" : False, "volunteer" : False})

def register(request):
	'''
	This method is used to register new user into the system as an admin or volunteer
	'''
	print request.user.username
	if request.user.username != '' and request.user.is_authenticated() and checkAdmin(request.user):
  		if request.method == 'POST':
    			userForm = UserForm(request.POST)
    			adminProfileForm = AdminProfileForm(request.POST)

    			if userForm.is_valid() and adminProfileForm.is_valid():
      				user = User.objects.create_user(first_name=userForm.cleaned_data['firstname'],last_name=userForm.cleaned_data['lastname'],
					  		email=userForm.cleaned_data['email'],username=userForm.cleaned_data['username'],
							password=userForm.cleaned_data['password'])

      				adminProfile = AdminProfile(user=user, address=adminProfileForm.cleaned_data['address'],
						location=adminProfileForm.cleaned_data['location'],state=adminProfileForm.cleaned_data['state'],
						organization=adminProfileForm.cleaned_data['organization'],phone=adminProfileForm.cleaned_data['phone'])

	     			adminProfile.save()
				orgObject=Organization.objects.get(Q(name=adminProfileForm.cleaned_data['organization']))
				orgObject.noOfVolunteers += 1
				orgObject.save()
      				return HttpResponse("You have registered, login available @ AdminUnit/")
  		else:
  			 userForm = UserForm()
  			 adminProfileForm = AdminProfileForm()
		return render(request, "AdminUnit/register.html",{ "userForm" : userForm , "adminProfileForm" : adminProfileForm , "admin" : True })
	else:
  		if request.method == 'POST':
    			userForm = UserForm(request.POST)
    			volunteerProfileForm = VolunteerProfileForm(request.POST)

	    		if userForm.is_valid() and volunteerProfileForm.is_valid():
      				user = User.objects.create_user(first_name=userForm.cleaned_data['firstname'],last_name=userForm.cleaned_data['lastname'],
					  		email=userForm.cleaned_data['email'],username=userForm.cleaned_data['username'],
							password=userForm.cleaned_data['password'])

      				volunteerProfile = VolunteerProfile(user=user, address=volunteerProfileForm.cleaned_data['address'],
					location=volunteerProfileForm.cleaned_data['location'],state=volunteerProfileForm.cleaned_data['state'],
					organization=volunteerProfileForm.cleaned_data['organization'], phone=volunteerProfileForm.cleaned_data['phone'])

      				volunteerProfile.save()
				orgObject=Organization.objects.get(Q(name=volunteerProfileForm.cleaned_data['organization']))
				orgObject.noOfVolunteers += 1
				orgObject.save()
      				return HttpResponse("You have registered, login available @ AdminUnit/")
		else:
  			 userForm = UserForm()
  			 volunteerProfileForm = VolunteerProfileForm()
		return render(request, "AdminUnit/register.html",{ "userForm" : userForm , "volunteerProfileForm" : volunteerProfileForm, "admin" : False })

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
@user_passes_test(checkAdmin, login_url='/AdminUnit/', redirect_field_name=None)
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
@user_passes_test(checkAdmin, login_url='/AdminUnit/', redirect_field_name=None)
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
			eventObject=Event.objects.get(eventName=jobsForm.cleaned_data['event'])
			eventObject.noOfVolunteersRequired+=jobsForm.cleaned_data['noOfVolunteersRequired']
			eventObject.save()
			users = VolunteerProfile.objects.all()
			email = []
			for user in users:
				email.append(user.user.email)
			textContent = 'Job Name : ' + jobsForm.cleaned_data['jobName'] + '\n' + 'Job Decription : ' + jobsForm.cleaned_data['jobDescription'] + '\n' + 'Start Time : ' + str(jobsForm.cleaned_data['startDate']) + '\n' + 'End Time : ' + str(jobsForm.cleaned_data['endDate']) + '\n' + 'Would you like to volunteer ?'
			send_mail('VMS: New Job', textContent, 'VMS Admin', email, fail_silently=False)
			return HttpResponse('Job Created')
  	else:
     		jobsForm = JobsForm(instance = jobInstance)
  	
	return render(request, "AdminUnit/jobs.html",{"jobsForm" : jobsForm})

@login_required
@user_passes_test(checkAdmin, login_url='/AdminUnit/', redirect_field_name=None)
def allEvents(request):
	'''
	Controller responsible for displaying all Events that have been registered, alongside will be displayed the links to edit/delete an event
	'''
  	allEvents = Event.objects.all()
  	return render(request, "AdminUnit/all_events.html", {"allEvents" : allEvents});

@login_required
@user_passes_test(checkAdmin, login_url='/AdminUnit/', redirect_field_name=None)
def allJobs(request):
	'''
	Controller responsible for displaying jobs registered across all Events that have been registered, alongside will be displayed the links to edit/delete the same
	'''
  	allJobs = Job.objects.all()
  	return render(request, "AdminUnit/all_jobs.html", {"allJobs" : allJobs});

@login_required
@user_passes_test(checkAdmin, login_url='/AdminUnit/', redirect_field_name=None)
def deleteEvent(request,eventId=None):
	'''
	Delete's an event with a given primary key
	'''
  	Event.objects.filter(pk=eventId).delete()
  	allEvents = Event.objects.all()
  	return render(request, "AdminUnit/all_events.html", {"allEvents" : allEvents});

@login_required
@user_passes_test(checkAdmin, login_url='/AdminUnit/', redirect_field_name=None)
def deleteJob(request,jobId=None):
	'''
	Delete's a job with a given primary key
	'''
	associatedEvent = Job.objects.get(pk=jobId).event.eventName
	event = Event.objects.get(eventName=associatedEvent)
	event.noOfVolunteersRequired-=Job.objects.get(pk=jobId).noOfVolunteersRequired
	event.save()
  	Job.objects.filter(pk=jobId).delete()
  	allJobs = Job.objects.all()
  	return render(request, "AdminUnit/all_jobs.html", {"allJobs" : allJobs});

@login_required
@user_passes_test(checkAdmin, login_url='/AdminUnit/', redirect_field_name=None)
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
@user_passes_test(checkAdmin, login_url='/AdminUnit/', redirect_field_name=None)
def allOrgs(request):
	'''
	Controller responsible for displaying all Events that have been registered, alongside will be displayed the links to edit/delete an event
	'''
  	allOrgs = Organization.objects.all()
  	return render(request, "AdminUnit/all_orgs.html", {"allOrgs" : allOrgs});

@login_required
@user_passes_test(checkAdmin, login_url='/AdminUnit/', redirect_field_name=None)
def deleteOrg(request,orgId=None):
	'''
	Delete's a job with a given primary key
	'''
  	Organization.objects.filter(pk=orgId).delete()
  	allOrgs = Organization.objects.all()
  	return render(request, "AdminUnit/all_orgs.html", {"allOrgs" : allOrgs});

@login_required
@user_passes_test(checkAdmin, login_url='/AdminUnit/', redirect_field_name=None)
def searchByEvent(request):
	if request.method == 'POST':
		selectEventForm = SelectEventForm(request.POST)
		if selectEventForm.is_valid():
			eventName = selectEventForm.cleaned_data['event']
			jobs = Job.objects.filter(event__eventName=eventName)
			selectEventForm = {}
			return render(request, "AdminUnit/search_by_events.html", {"jobs" : jobs, "selectEventForm" : selectEventForm})
		else:
			return render(request, "AdminUnit/search_by_events.html", {"jobs" : {}, "selectEventForm" : selectEventForm})
	else:
		selectEventForm = SelectEventForm()
		jobs = {}
		return render(request, "AdminUnit/search_by_events.html", {"jobs" : jobs, "selectEventForm" : selectEventForm});

@login_required
@user_passes_test(checkAdmin, login_url='/AdminUnit/', redirect_field_name=None)
def searchByTime(request):
	if request.method == 'POST':
		selectTimeForm = SelectTimeForm(request.POST)
		if selectTimeForm.is_valid():
			startTime = selectTimeForm.cleaned_data['startTime']
			endTime = selectTimeForm.cleaned_data['endTime']
			jobs = Job.objects.filter(startDate__gte=startTime,endDate__lte=endTime)
			selectTimeForm = {}
			return render(request, "AdminUnit/search_by_time.html", {"jobs" : jobs, "selectTimeForm" : selectTimeForm});
		else:
			return render(request, "AdminUnit/search_by_time.html", {"jobs" : {}, "selectTimeForm" : selectTimeForm});
	else:
		selectTimeForm = SelectTimeForm()
		jobs = {}
		return render(request, "AdminUnit/search_by_time.html", {"jobs" : jobs, "selectTimeForm" : selectTimeForm});

@login_required
@user_passes_test(checkAdmin, login_url='/AdminUnit/', redirect_field_name=None)
def searchEmployeeByOrg(request):
	if request.method == 'POST':
		selectOrgForm = SelectOrgForm(request.POST)
		if selectOrgForm.is_valid():
			orgName = selectOrgForm.cleaned_data['org']
			users = VolunteerProfile.objects.filter(organization__name=orgName)
			selectOrgForm = {}
			return render(request, "AdminUnit/search_by_org.html", {"users" : users, "selectOrgForm" : selectOrgForm});
		else:
			return render(request, "AdminUnit/search_by_org.html", {"users" : {}, "selectOrgForm" : selectOrgForm});
	else:
		selectOrgForm = SelectOrgForm()
		users = {}
		return render(request, "AdminUnit/search_by_org.html", {"users" : users, "selectOrgForm" : selectOrgForm});

@login_required
@user_passes_test(checkAdmin, login_url='/AdminUnit/', redirect_field_name=None)
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
			 event = shiftForm.cleaned_data['event'].eventName
			 job = shiftForm.cleaned_data['job'].jobName
			 volunteer = shiftForm.cleaned_data['volunteer'].user.username
			 hours = shiftForm.cleaned_data['hours']
			 startDate = Job.objects.get(event__eventName=event,jobName=job).startDate
			 endDate = Job.objects.get(event__eventName=event,jobName=job).endDate
			 email = [VolunteerProfile.objects.get(user__username=volunteer).user.email]
			 textContent = 'Event : ' + event + '\n' + 'Job Name : ' + job + '\n' + 'Hours Assigned : ' + str(hours) + '\n' + 'Job Start Date : ' + str(startDate) +'\n' + 'Job End Date : ' + str(endDate)
			 send_mail('VMS: You\'ve been assigned a job', textContent, 'VMS Admin', list(email), fail_silently=False)
			 return HttpResponse("Shift Created/Edited")
  	
	# to handle a GET Request
	else:
    		shiftForm = ShiftForm(instance=shiftInstance)

	return render(request, "AdminUnit/shift.html", {"shiftForm" : shiftForm})

@login_required
@user_passes_test(checkAdmin, login_url='/AdminUnit/', redirect_field_name=None)
def allShifts(request):
	'''
	Controller responsible for displaying all Events that have been registered, alongside will be displayed the links to edit/delete an event
	'''
  	allShifts = Shift.objects.all()
  	return render(request, "AdminUnit/all_shifts.html", {"allShifts" : allShifts});

@login_required
@user_passes_test(checkAdmin, login_url='/AdminUnit/', redirect_field_name=None)
def deleteShift(request,shiftId=None):
	'''
	Delete's a job with a given primary key
	'''
  	Shift.objects.filter(pk=shiftId).delete()
  	allShifts = Shift.objects.all()
  	return render(request, "AdminUnit/all_shifts.html", {"allShifts" : allShifts});

@login_required
@user_passes_test(checkAdmin, login_url='/AdminUnit/', redirect_field_name=None)
def createShift(request, jobId=None, eventId=None, userName=None):
	if Shift.objects.filter(event__pk=eventId,job__pk=jobId,volunteer__user__username=userName).count() == 0:
	      	shift = Shift(event=Event.objects.get(pk=eventId),job=Job.objects.get(pk=jobId),volunteer=VolunteerProfile.objects.get(user__username=userName),hours=1)
		shift.save()
		return HttpResponse("Shift Created");
	else:
		return HttpResponse("Shift with same username, eventname, jobname exists");

@login_required
@user_passes_test(checkAdmin, login_url='/AdminUnit/', redirect_field_name=None)
def reportHoursByOrg(request):
	if request.method == 'POST':
		selectHoursForm = SelectHoursForm(request.POST)
		if selectHoursForm.is_valid():
			fromHours = selectHoursForm.cleaned_data['fromHours']
			toHours = selectHoursForm.cleaned_data['toHours']
			shifts = Shift.objects.all()
			counts = {}
			details = {}
			for shift in shifts:
				org = shift.volunteer.organization.name
				if org in counts:
					counts[org]+=shift.hours
					details[org].append((shift.volunteer.user.username, shift.hours))
				else:
					counts[org]=shift.hours
					details[org]=[]
					details[org].append((shift.volunteer.user.username, shift.hours))
			data = []
			for org in counts:
				if counts[org] >= fromHours and counts[org] <= toHours:
					data.append([org,counts[org]])
				else:
					del(details[org])
			return render(request, "AdminUnit/report_hours_by_org.html", {"values" : data, "selectHoursForm" : {}, "details" : details})
		else:
			return render(request, "AdminUnit/report_hours_by_org.html", {"values" : {}, "selectHoursForm" : selectHoursForm, "details" : {}})
	else:
		selectHoursForm = SelectHoursForm()
		return render(request, "AdminUnit/report_hours_by_org.html", {"values" : {}, "selectHoursForm" : selectHoursForm, "details" : {}})

@login_required
@user_passes_test(checkAdmin, login_url='/AdminUnit/', redirect_field_name=None)
def reportVolunteersByOrg(request):
	users = AdminProfile.objects.all()
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
@user_passes_test(checkAdmin, login_url='/AdminUnit/', redirect_field_name=None)
def reportHoursByEvent(request):
	if request.method == 'POST':
		selectEventForm = SelectEventForm(request.POST)
		if selectEventForm.is_valid():
			eventName = selectEventForm.cleaned_data['event']
			shifts = Shift.objects.filter(event__eventName=eventName)
			counts = {}
			details = {}
			for shift in shifts:
				org = shift.volunteer.organization.name
				if org in counts:
					counts[org]+=shift.hours
					details[org].append((shift.volunteer.user.username, shift.hours))
				else:
					counts[org]=shift.hours
					details[org]=[]
					details[org].append((shift.volunteer.user.username, shift.hours))
		
			data = []
			for org in counts:
				data.append([org,counts[org]])
			selectEventForm = {}
			return render(request, "AdminUnit/report_hours_by_event.html", {"values" : data, "selectEventForm" : selectEventForm, "details" : details})
		else:
			return render(request, "AdminUnit/report_hours_by_event.html", {"values" : {}, "selectEventForm" : selectEventForm, "details" : {}})
	else:
		selectEventForm = SelectEventForm()
		data = []
		return render(request, "AdminUnit/report_hours_by_event.html", {"values" : data, "selectEventForm" : selectEventForm, "details" : {}})

@login_required
@user_passes_test(checkAdmin, login_url='/AdminUnit/', redirect_field_name=None)
def reportHoursByTime(request):
	if request.method == 'POST':
		selectTimeForm = SelectTimeForm(request.POST)
		if selectTimeForm.is_valid():
			startTime = selectTimeForm.cleaned_data['startTime']
			endTime = selectTimeForm.cleaned_data['endTime']
			shifts = Shift.objects.filter(event__startDate__gte=startTime,event__endDate__lte=endTime)
			counts = {}
			details = {}	
			for shift in shifts:
				org = shift.volunteer.organization.name
				if org in counts:
					counts[org]+=shift.hours
					details[org].append((shift.volunteer.user.username, shift.hours))
				else:
					counts[org]=shift.hours
					details[org]=[]
					details[org].append((shift.volunteer.user.username, shift.hours))
		
			data = []
			for org in counts:
				data.append([org,counts[org]])
			selectTimeForm = {}
			return render(request, "AdminUnit/report_hours_by_time.html", {"values" : data, "selectTimeForm" : selectTimeForm, "details" : details})
		else:
			return render(request, "AdminUnit/report_hours_by_time.html", {"values" : {}, "selectTimeForm" : selectTimeForm, "details" : {}})
	else:
		selectTimeForm = SelectTimeForm()
		data = []
		return render(request, "AdminUnit/report_hours_by_time.html", {"values" : data, "selectTimeForm" : selectTimeForm, "details" : {}})

@login_required
@user_passes_test(checkAdmin, login_url='/AdminUnit/', redirect_field_name=None)
def reportHoursByTimeAndOrg(request):
	if request.method == 'POST':
		selectTimeForm = SelectTimeForm(request.POST)
		selectOrgForm = SelectOrgForm(request.POST)
		if selectTimeForm.is_valid() and selectOrgForm.is_valid():
			startTime = selectTimeForm.cleaned_data['startTime']
			endTime = selectTimeForm.cleaned_data['endTime']
			organization = selectOrgForm.cleaned_data['org']
			shifts = Shift.objects.filter(event__startDate__gte=startTime,event__endDate__lte=endTime,volunteer__organization__name=organization)
			counts = {}
			details = {}
			for shift in shifts:
				eventname = shift.event.eventName
				username = shift.volunteer.user.username
				if username in counts:
					counts[username]+=shift.hours
					details[username].append((eventname, shift.hours))
				else:
					counts[username]=shift.hours
					details[username]=[]
					details[username].append((eventname, shift.hours))
		
			data = []
			for username in counts:
				data.append([username,counts[username]])
			selectTimeForm = {}
			return render(request, "AdminUnit/report_hours_by_time_and_org.html", {"values" : data, "selectTimeForm" : {}, "selectOrgForm" : {},  "details" : details})
		else:
			return render(request, "AdminUnit/report_hours_by_time_and_org.html", {"values" : {}, "selectTimeForm" : selectTimeForm, "selectOrgForm" : selectOrgForm,  "details" : {}})
	else:
		selectTimeForm = SelectTimeForm()
		selectOrgForm = SelectOrgForm()
		data = []
		return render(request, "AdminUnit/report_hours_by_time_and_org.html", {"values" : data, "selectTimeForm" : selectTimeForm, "selectOrgForm" : selectOrgForm,  "details" : {}})
