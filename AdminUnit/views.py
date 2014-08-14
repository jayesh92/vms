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
    """
    This method is used by user_passes_test decorator to
    distinguish between admin user and volunteer user.
    It returns true if user object is a super user or
    member of AdminProfile table
    """
    if user:
        if user.is_superuser or AdminProfile.objects.filter(
                user__username=user.username).count() == 1:
            return True
    return False


def checkVolunteer(user):
    """
    This method checks if passes uder object is a registerd
    volunteer user or not
    """
    if user:
        if VolunteerProfile.objects.filter(
                user__username=user.username).count() == 1:
            return True
    return False


def index(request):
    """
    Method displays the index page(dashboard) to the user
    as per his access rights (Volunteer/Admin). Distinction
    is done on the basis of checkAdmin and checkVolunteer
    methods
    """
    if request.user:
        if checkAdmin(request.user):
            return render(request,
                          "AdminUnit/index.html",
                          {"admin": True,
                           "volunteer": False})
        elif checkVolunteer(request.user):
            return render(request,
                          "AdminUnit/index.html",
                          {"admin": False,
                           "volunteer": True})
    return render(request,
                  "AdminUnit/index.html",
                  {"admin": False,
                   "volunteer": False})


def register(request):
    """
    This method is responsible for siplaying the register user view
    Register Admin or volunteer is judged on the basis of users 
    access rights.
    Only if user is registered and logged in and registered as an
    admin user, he/she is allowed to register others as an admin user
    """
    if request.user.username != '' and request.user.is_authenticated(
    ) and checkAdmin(request.user):
        if request.method == 'POST':
            userForm = UserForm(request.POST)
            adminProfileForm = AdminProfileForm(request.POST)

            if userForm.is_valid() and adminProfileForm.is_valid():
                user = User.objects.create_user(
                    first_name=userForm.cleaned_data['firstname'],
                    last_name=userForm.cleaned_data['lastname'],
                    email=userForm.cleaned_data['email'],
                    username=userForm.cleaned_data['username'],
                    password=userForm.cleaned_data['password'])

                adminProfile = AdminProfile(
                    user=user,
                    address=adminProfileForm.cleaned_data['address'],
                    location=adminProfileForm.cleaned_data['location'],
                    state=adminProfileForm.cleaned_data['state'],
                    organization=adminProfileForm.cleaned_data['organization'],
                    phone=adminProfileForm.cleaned_data['phone'])

                adminProfile.save()
                orgObject = Organization.objects.get(
                    Q(name=adminProfileForm.cleaned_data['organization']))
                orgObject.noOfVolunteers += 1
                orgObject.save()
                return HttpResponse(
                    "You have registered, login available @ AdminUnit/")
        else:
            userForm = UserForm()
            adminProfileForm = AdminProfileForm()
        return render(request,
                      "AdminUnit/register.html",
                      {"userForm": userForm,
                       "adminProfileForm": adminProfileForm,
                       "admin": True})
    else:
        if request.method == 'POST':
            userForm = UserForm(request.POST)
            volunteerProfileForm = VolunteerProfileForm(request.POST)

            if userForm.is_valid() and volunteerProfileForm.is_valid():
                user = User.objects.create_user(
                    first_name=userForm.cleaned_data['firstname'],
                    last_name=userForm.cleaned_data['lastname'],
                    email=userForm.cleaned_data['email'],
                    username=userForm.cleaned_data['username'],
                    password=userForm.cleaned_data['password'])

                volunteerProfile = VolunteerProfile(
                    user=user,
                    address=volunteerProfileForm.cleaned_data['address'],
                    location=volunteerProfileForm.cleaned_data['location'],
                    state=volunteerProfileForm.cleaned_data['state'],
                    organization=volunteerProfileForm.cleaned_data['organization'],
                    phone=volunteerProfileForm.cleaned_data['phone'])

                volunteerProfile.save()
                orgObject = Organization.objects.get(
                    Q(name=volunteerProfileForm.cleaned_data['organization']))
                orgObject.noOfVolunteers += 1
                orgObject.save()
                return HttpResponse(
                    "You have registered, login available @ AdminUnit/")
        else:
            userForm = UserForm()
            volunteerProfileForm = VolunteerProfileForm()
        return render(request,
                      "AdminUnit/register.html",
                      {"userForm": userForm,
                       "volunteerProfileForm": volunteerProfileForm,
                       "admin": False})


def login_process(request):
    """
    Checks user's credentials and logs him to admin or volunteer
    dashboard accordingly.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
		return HttpResponseRedirect('/AdminUnit/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'AdminUnit/login.html')


@login_required
def logout_process(request):
    """
    Logout a user object
    """
    logout(request)
    return HttpResponseRedirect('/AdminUnit/')


@login_required
@user_passes_test(checkAdmin,login_url='/AdminUnit/',redirect_field_name=None)
def editEvent(request, eventId=None):
    """
    Use to Edit/Create Event Objects
    """
    if eventId:
        eventInstance = Event.objects.get(pk=eventId)
    else:
        eventInstance = None

    if request.method == 'POST':
        eventForm = EventForm(request.POST, instance=eventInstance)
        if eventForm.is_valid():
            newRecord = eventForm.save()
            return HttpResponse("Event Created/Edited")
    else:
        eventForm = EventForm(instance=eventInstance)

    return render(request, "AdminUnit/event.html", {"eventForm": eventForm})


@login_required
@user_passes_test(checkAdmin,login_url='/AdminUnit/',redirect_field_name=None)
def job(request, jobId=None):
    """
    Used to Edit/Create Job
    """
    if jobId:
        jobInstance = Job.objects.get(pk=jobId)
    else:
        jobInstance = None

    if request.method == 'POST':
        jobsForm = JobsForm(request.POST, instance=jobInstance)
        if jobsForm.is_valid():
            newRecord = jobsForm.save()
            return HttpResponse('Job Created')
    else:
        jobsForm = JobsForm(instance=jobInstance)
    return render(request, "AdminUnit/jobs.html", {"jobsForm": jobsForm})


@login_required
@user_passes_test(checkAdmin,login_url='/AdminUnit/',redirect_field_name=None)
def allEvents(request):
    """
    This method is responsible for the all events view
    """
    allEvents = Event.objects.all()
    return render(request,
                  "AdminUnit/all_events.html",
                  {"allEvents": allEvents})


@login_required
@user_passes_test(checkAdmin,login_url='/AdminUnit/',redirect_field_name=None)
def allJobs(request):
    """
    This method is responsible for the all jobs view
    """
    allJobs = Job.objects.all()
    return render(request,
                  "AdminUnit/all_jobs.html",
                  {"allJobs": allJobs})


@login_required
@user_passes_test(checkAdmin,login_url='/AdminUnit/',redirect_field_name=None)
def deleteEvent(request, eventId=None):
    """
    Delete's an event with a given primary key
    """
    if eventId != None:
	    Event.objects.filter(pk=eventId).delete()
    return HttpResponseRedirect('/AdminUnit/allEvents/')


@login_required
@user_passes_test(checkAdmin,login_url='/AdminUnit/',redirect_field_name=None)
def deleteJob(request, jobId=None):
    """
    Delete's a job with a given primary key
    """
    if jobId != None:
        associatedEvent = Job.objects.get(pk=jobId).event.eventName
        event = Event.objects.get(eventName=associatedEvent)
        event.noOfVolunteersAssigned -= Job.objects.get(
            pk=jobId).noOfVolunteersAssigned
        event.noOfVolunteersWorked -= Job.objects.get(
            pk=jobId).noOfVolunteersWorked
        event.save()
        Job.objects.filter(pk=jobId).delete()
    return HttpResponseRedirect('/AdminUnit/allJobs/')


@login_required
@user_passes_test(checkAdmin,login_url='/AdminUnit/',redirect_field_name=None)
def editOrg(request, orgId=None):
    """
    Use to Edit/Create Organization
    """
    if orgId:
        orgInstance = Organization.objects.get(pk=orgId)
    else:
        orgInstance = None

    if request.method == 'POST':
        orgForm = OrgForm(request.POST, instance=orgInstance)
        if orgForm.is_valid():
            newRecord = orgForm.save()
            return HttpResponse("Org Created/Edited")
    else:
        orgForm = OrgForm(instance=orgInstance)
    return render(request, "AdminUnit/org.html", {"orgForm": orgForm})


@login_required
@user_passes_test(checkAdmin,login_url='/AdminUnit/',redirect_field_name=None)
def allOrgs(request):
    """
    This method is responsible for displating th all Organizations view
    """
    allOrgs = Organization.objects.all()
    return render(request, "AdminUnit/all_orgs.html", {"allOrgs": allOrgs})


@login_required
@user_passes_test(checkAdmin,login_url='/AdminUnit/',redirect_field_name=None)
def deleteOrg(request, orgId=None):
    """
    Delete's an org with a given primary key
    """
    Organization.objects.filter(pk=orgId).delete()
    return HttpResponseRedirect("/AdminUnit/allOrgs")


@login_required
@user_passes_test(checkVolunteer,login_url='/AdminUnit/',redirect_field_name=None)
def searchByEvent(request):
    """
    This method displays all jobs inside an event.
    Will be used by volunteer's to search Shifts in an event
    """
    if request.method == 'POST':
        selectEventForm = SelectEventForm(request.POST)
        if selectEventForm.is_valid():
            eventName = selectEventForm.cleaned_data['event']
            shifts = Shift.objects.filter(event__eventName=eventName)
            selectEventForm = {}
            return render(request,
                          "AdminUnit/search_by_events.html",
                          {"shifts": shifts,
                           "selectEventForm": selectEventForm})
        else:
            return render(request,
                          "AdminUnit/search_by_events.html",
                          {"shifts": {},
                           "selectEventForm": selectEventForm})
    else:
        selectEventForm = SelectEventForm()
        jobs = {}
        return render(request,
                      "AdminUnit/search_by_events.html",
                      {"shifts": jobs,
                       "selectEventForm": selectEventForm})


@login_required
@user_passes_test(checkVolunteer,login_url='/AdminUnit/',redirect_field_name=None)
def searchByTime(request):
    """
    This method displays all jobs within a time range.
    Will be used by volunteer's to search jobs
    """
    if request.method == 'POST':
        selectTimeForm = SelectTimeForm(request.POST)
        if selectTimeForm.is_valid():
            startTime = selectTimeForm.cleaned_data['startTime']
            endTime = selectTimeForm.cleaned_data['endTime']
            shifts = Shift.objects.filter(
                startTime__gte=startTime,
                endTime__lte=endTime)
            selectTimeForm = {}
            return render(request,
                          "AdminUnit/search_by_time.html",
                          {"shifts": shifts,
                           "selectTimeForm": selectTimeForm})
        else:
            return render(request,
                          "AdminUnit/search_by_time.html",
                          {"shifts": {},
                           "selectTimeForm": selectTimeForm})
    else:
        selectTimeForm = SelectTimeForm()
        shifts = {}
        return render(request,
                      "AdminUnit/search_by_time.html",
                      {"shifts": shifts,
                       "selectTimeForm": selectTimeForm})


@login_required
@user_passes_test(checkAdmin,login_url='/AdminUnit/',redirect_field_name=None)
def searchEmployeeByOrg(request):
    """
    This method displays all employees belonging to an Org.
    """
    if request.method == 'POST':
        selectOrgForm = SelectOrgForm(request.POST)
        if selectOrgForm.is_valid():
            orgName = selectOrgForm.cleaned_data['org']
            users = VolunteerProfile.objects.filter(organization__name=orgName)
            selectOrgForm = {}
            return render(request,
                          "AdminUnit/search_by_org.html",
                          {"users": users,
                           "selectOrgForm": selectOrgForm})
        else:
            return render(request,
                          "AdminUnit/search_by_org.html",
                          {"users": {},
                           "selectOrgForm": selectOrgForm})
    else:
        selectOrgForm = SelectOrgForm()
        users = {}
        return render(request,
                      "AdminUnit/search_by_org.html",
                      {"users": users,
                       "selectOrgForm": selectOrgForm})


@login_required
@user_passes_test(checkAdmin,login_url='/AdminUnit/',redirect_field_name=None)
def manageShift(request, shiftId=None):
    """
    Use to Edit/Create Shifts
    Used by admin to assign shifts to voluneers
    """
    if shiftId:
        shiftInstance = Shift.objects.get(pk=shiftId)
    else:
        shiftInstance = None

    if request.method == 'POST':
        shiftForm = ShiftForm(request.POST, instance=shiftInstance)
        if shiftForm.is_valid():
            newRecord = shiftForm.save()
            return HttpResponse("Shift Created/Edited")
    else:
        shiftForm = ShiftForm(instance=shiftInstance)

    return render(request, "AdminUnit/shift.html", {"shiftForm": shiftForm})


@login_required
@user_passes_test(checkAdmin,login_url='/AdminUnit/',redirect_field_name=None)
def allShifts(request):
    """
    Controller for all Shifts views
    """
    allShifts = Shift.objects.all()
    return render(request,
                  "AdminUnit/all_shifts.html",
                  {"allShifts": allShifts})


@login_required
@user_passes_test(checkAdmin,login_url='/AdminUnit/',redirect_field_name=None)
def deleteShift(request, shiftId=None):
    """
    Delete's a shift with a given primary key
    """
    if shiftId != None and Shift.objects.filter(pk=shiftId).count() == 1:
	    Shift.objects.filter(pk=shiftId).delete()
    return HttpResponseRedirect('/AdminUnit/allShifts/')


@login_required
@user_passes_test(checkVolunteer,login_url='/AdminUnit/',redirect_field_name=None)
def createSat(request, shiftId=None, userName=None):
    if shiftId == None or userName == '':
        return HttpResponseRedirect('/AdminUnit/CreateSat/')
    if VolunteerProfile.objects.filter(user__username=userName).count == 0:
        return HttpResponse('Matching volunteer Profile not found')
    shift=Shift.objects.get(pk=shiftId)
    volunteer=VolunteerProfile.objects.get(user__username=userName)
    if SAT.objects.filter(shift=shift,volunteer=volunteer).count() == 1:
        return HttpResponse('SAT entry with given shift and volunteer already exists')
    startTime = shift.startTime
    endTime = shift.endTime
    diff = endTime-startTime
    hours = "%.2f" % (diff.total_seconds()/3600.0)
    SAT.objects.create(shift=shift, volunteer=volunteer, startTime=shift.startTime, endTime=shift.endTime, hours=hours)

    job = Job.objects.get(jobName=shift.job.jobName,event__eventName=shift.event.eventName)
    job.noOfVolunteersAssigned += 1
    job.save()

    event = Event.objects.get(eventName=shift.event.eventName)
    event.noOfVolunteersAssigned += 1
    event.save()
    return HttpResponse('SAT entry created successfully')


@login_required
@user_passes_test(checkAdmin,login_url='/AdminUnit/',redirect_field_name=None)
def sat(request, satId=None):
    """
    Use to Edit/Create SATs
    Used by admin to assign shifts to voluneers
    """
    if satId:
        satInstance = SAT.objects.get(pk=satId)
    else:
        satInstance = None

    if request.method == 'POST':
        satForm = SATForm(request.POST, instance=satInstance)
        if satForm.is_valid():
            eventName = satForm.cleaned_data['shift'].event.eventName
            jobName = satForm.cleaned_data['shift'].job.jobName
            startTime = satForm.cleaned_data['shift'].startTime
            endTime = satForm.cleaned_data['shift'].endTime
            diff = endTime-startTime
            hours = "%.2f" % (diff.total_seconds()/3600.0)
            SAT.objects.create(shift=satForm.cleaned_data['shift'],
                volunteer=satForm.cleaned_data['volunteer'],
                startTime=startTime,
                endTime=endTime,
                hours=hours
            )
           
            job = Job.objects.get(jobName=jobName,event__eventName=eventName)
            job.noOfVolunteersAssigned += 1
            job.save()

            event = Event.objects.get(eventName=eventName)
            event.noOfVolunteersAssigned += 1
            event.save()

            email = [satForm.cleaned_data['volunteer'].user.email]
            textContent = 'Hi ' + satForm.cleaned_data['volunteer'].user.username + '!' + '\n\n' + 'Event : ' + eventName + '\n' + 'Job Name : ' + jobName + '\n' +  'Shift Start Time : ' + str(startTime) + '\n' + 'Shift End Time : ' + str(endTime)
            send_mail(
                'VMS: You\'ve been assigned a Shift',
                textContent,
                'VMS Admin',
                list(email),
                fail_silently=False)
            return HttpResponse("SAT Created/Edited")
    else:
        satForm = SATForm(instance=satInstance)

    return render(request, "AdminUnit/sat.html", {"satForm": satForm})


@login_required
@user_passes_test(checkAdmin,login_url='/AdminUnit/',redirect_field_name=None)
def allSats(request):
    """
    Controller for all Shifts views
    """
    allSats = SAT.objects.all()
    return render(request,
                  "AdminUnit/all_sats.html",
                  {"allSats": allSats})


@login_required
@user_passes_test(checkAdmin,login_url='/AdminUnit/',redirect_field_name=None)
def deleteSat(request, satId=None):
    """
    """
    if satId != None:
        eventName=SAT.objects.get(pk=satId).shift.event.eventName
        jobName=SAT.objects.get(pk=satId).shift.job.jobName
        job = Job.objects.get(jobName=jobName,event__eventName=eventName)
        job.noOfVolunteersAssigned -= 1
        job.save()
        event = Event.objects.get(eventName=eventName)
        event.noOfVolunteersAssigned -= 1
        event.save()
        SAT.objects.filter(pk=satId).delete()
    return HttpResponseRedirect('/AdminUnit/allSats/')


@login_required
def wlt(request, wltId=None):
    """
    Use to Edit/Create SATs
    Used by admin to assign shifts to voluneers
    """
    if checkAdmin(request.user):
        if wltId:
            wltInstance = WLT.objects.get(pk=wltId)
        else:
            wltInstance = None

        if request.method == 'POST':
            wltForm = WLTAdminForm(request.POST, instance=wltInstance)
            if wltForm.is_valid():
                newRecord = wltForm.save()
                startTime = wltForm.cleaned_data['startTime']
                endTime = wltForm.cleaned_data['endTime']
                diff = endTime-startTime
                hours = "%.2f" % (diff.total_seconds()/3600.0)
                newRecord.hours = hours
                newRecord.save()
                return HttpResponse("WLT Created/Edited")
        else:
            wltForm = WLTAdminForm(instance=wltInstance)
        return render(request, "AdminUnit/wlt.html", {"wltForm": wltForm})
    else:
        if wltId:
            wltInstance = WLT.objects.get(pk=wltId)
            if WLT.objects.get(pk=wltId).volunteer.user.username != request.user.username:
                return HttpResponse("Access Denied")
        else:
            wltInstance = None

        if request.method == 'POST':
            wltForm = WLTVolunteerForm(request.POST, instance=wltInstance)
            if wltForm.is_valid():
                shift = wltForm.cleaned_data['shift']
                volunteer = VolunteerProfile.objects.get(user__username=request.user.username)
                startTime = wltForm.cleaned_data['startTime']
                endTime = wltForm.cleaned_data['endTime']
                diff = endTime-startTime
                hours = "%.2f" % (diff.total_seconds()/3600.0)
                if WLT.objects.filter(shift=shift,volunteer=volunteer).count() == 0:
                    WLT.objects.create(shift=shift,volunteer=volunteer,startTime=startTime,
                        endTime=endTime,hours=hours)
                else:
                    wltObject = WLT.objects.get(shift=shift,volunteer=volunteer)
                    wltObject.startTime = startTime
                    wltObject.endTime = endTime
                    wltObject.hours = hours
                    wltObject.save()
                return HttpResponse("WLT Created/Edited")
        else:
            wltForm = WLTVolunteerForm(instance=wltInstance)
        return render(request, "AdminUnit/wlt.html", {"wltForm": wltForm})


@login_required
def allWlts(request):
    """
    Controller for all Shifts views
    """
    if checkAdmin(request.user):
        allWlts = WLT.objects.all()
    else:
        allWlts = WLT.objects.filter(volunteer__user__username=request.user.username)
    return render(request,
                  "AdminUnit/all_wlts.html",
                  {"allWlts": allWlts})


@login_required
@user_passes_test(checkAdmin,login_url='/AdminUnit/',redirect_field_name=None)
def deleteWlt(request, wltId=None):
    """
    Delete's a shift with a given primary key
    """
    if checkVolunteer(request.user):
        if WLT.objects.get(pk=wltId).volunteer.user.username != request.user.username:
            return HttpResponse("Access Denied")
    if wltId != None:
	    WLT.objects.filter(pk=wltId).delete()
    return HttpResponseRedirect('/AdminUnit/allWlts/')

@login_required
@user_passes_test(checkVolunteer,login_url='/AdminUnit/',redirect_field_name=None)
def mySats(request):
    sats = SAT.objects.filter(volunteer__user__username=request.user.username)
    return render(request, "AdminUnit/my_sats.html", { "sats" : sats })

@login_required
@user_passes_test(checkAdmin,login_url='/AdminUnit/',redirect_field_name=None)
def reportHoursByOrg(request):
    """
    Reports total number of hours worked by all volunteers
    grouped by organization
    Gives Graphical as well as textual content
    """
    if request.method == 'POST':
        selectHoursForm = SelectHoursForm(request.POST)
        if selectHoursForm.is_valid():
            fromHours = selectHoursForm.cleaned_data['fromHours']
            toHours = selectHoursForm.cleaned_data['toHours']
            shifts = WLT.objects.all()
            counts = {}
            details = {}
            for shift in shifts:
                org = shift.volunteer.organization.name
                if org in counts:
                    counts[org] += shift.hours
                    details[org].append(shift)
                else:
                    counts[org] = shift.hours
                    details[org] = []
                    details[org].append(shift)
            data = []
            for org in counts:
                if counts[org] >= fromHours and counts[org] <= toHours:
                    data.append([org, counts[org]])
                else:
                    del(details[org])
            return render(request,
                          "AdminUnit/report_hours_by_org.html",
                          {"values": data,
                           "selectHoursForm": {},
                              "details": details})
        else:
            return render(request,
                          "AdminUnit/report_hours_by_org.html",
                          {"values": {},
                           "selectHoursForm": selectHoursForm,
                           "details": {}})
    else:
        selectHoursForm = SelectHoursForm()
        return render(request,
                      "AdminUnit/report_hours_by_org.html",
                      {"values": {},
                       "selectHoursForm": selectHoursForm,
                       "details": {}})


@login_required
@user_passes_test(checkAdmin,login_url='/AdminUnit/',redirect_field_name=None)
def reportVolunteersByOrg(request):
    """
    Reports total nu,ber of volunteers grouped by organization
    """
    users = VolunteerProfile.objects.all()
    counts = {}
    details = {}
    for user in users:
        org = user.organization.name
        if org in counts:
            counts[org] += 1
            details[org].append(user)
        else:
            counts[org] = 1
            details[org] = []
            details[org].append(user)
    data = []
    for org in counts:
        data.append([org, counts[org]])
    values = {'values': data, 'details' : details}
    return render(request, "AdminUnit/report_volunteers_by_org.html", values)


@login_required
@user_passes_test(checkAdmin,login_url='/AdminUnit/',redirect_field_name=None)
def reportHoursByEvent(request):
    """
    Total numer of hours contributed by each organization during the
    given event.
    """
    if request.method == 'POST':
        selectEventForm = SelectEventForm(request.POST)
        if selectEventForm.is_valid():
            eventName = selectEventForm.cleaned_data['event']
            shifts = WLT.objects.filter(shift__event__eventName=eventName)
            counts = {}
            details = {}
            for shift in shifts:
                org = shift.volunteer.organization.name
                if org in counts:
                    counts[org] += shift.hours
                    details[org].append(shift)
                else:
                    counts[org] = shift.hours
                    details[org] = []
                    details[org].append(shift)

            data = []
            for org in counts:
                data.append([org, counts[org]])
            selectEventForm = {}
            return render(request,
                          "AdminUnit/report_hours_by_event.html",
                          {"values": data,
                           "selectEventForm": selectEventForm,
                           "details": details})
        else:
            return render(request,
                          "AdminUnit/report_hours_by_event.html",
                          {"values": {},
                           "selectEventForm": selectEventForm,
                           "details": {}})
    else:
        selectEventForm = SelectEventForm()
        data = []
        return render(request,
                      "AdminUnit/report_hours_by_event.html",
                      {"values": data,
                       "selectEventForm": selectEventForm,
                       "details": {}})


@login_required
@user_passes_test(checkAdmin,login_url='/AdminUnit/',redirect_field_name=None)
def reportHoursByTime(request):
    """
    Reports total numer of hours contributed by employees across
    all events occured during the given dates, Grouped by Organizations
    """
    if request.method == 'POST':
        selectTimeForm = SelectTimeForm(request.POST)
        if selectTimeForm.is_valid():
            startTime = selectTimeForm.cleaned_data['startTime']
            endTime = selectTimeForm.cleaned_data['endTime']
            shifts = WLT.objects.filter(
                startTime__gte=startTime,
                endTime__lte=endTime)
            counts = {}
            details = {}
            for shift in shifts:
                org = shift.volunteer.organization.name
                if org in counts:
                    counts[org] += shift.hours
                    details[org].append(shift)
                else:
                    counts[org] = shift.hours
                    details[org] = []
                    details[org].append(shift)

            data = []
            for org in counts:
                data.append([org, counts[org]])
            selectTimeForm = {}
            return render(request,
                          "AdminUnit/report_hours_by_time.html",
                          {"values": data,
                           "selectTimeForm": selectTimeForm,
                           "details": details})
        else:
            return render(request,
                          "AdminUnit/report_hours_by_time.html",
                          {"values": {},
                           "selectTimeForm": selectTimeForm,
                           "details": {}})
    else:
        selectTimeForm = SelectTimeForm()
        data = []
        return render(request,
                      "AdminUnit/report_hours_by_time.html",
                      {"values": data,
                       "selectTimeForm": selectTimeForm,
                       "details": {}})


@login_required
@user_passes_test(checkAdmin,login_url='/AdminUnit/',redirect_field_name=None)
def reportHoursByTimeAndOrg(request):
    """
    Total number of hours contributed by each employee of
    given organization across all events occured during
    the given timestamps
    """
    if request.method == 'POST':
        selectTimeForm = SelectTimeForm(request.POST)
        selectOrgForm = SelectOrgForm(request.POST)
        if selectTimeForm.is_valid() and selectOrgForm.is_valid():
            startTime = selectTimeForm.cleaned_data['startTime']
            endTime = selectTimeForm.cleaned_data['endTime']
            organization = selectOrgForm.cleaned_data['org']
            shifts = WLT.objects.filter(
                startTime__gte=startTime,
                endTime__lte=endTime,
                volunteer__organization__name=organization)
            counts = {}
            details = {}
            for shift in shifts:
                eventname = shift.shift.event.eventName
                username = shift.volunteer.user.username
                if username in counts:
                    counts[username] += shift.hours
                    details[username].append(shift)
                else:
                    counts[username] = shift.hours
                    details[username] = []
                    details[username].append(shift)

            data = []
            for username in counts:
                data.append([username, counts[username]])
            selectTimeForm = {}
            return render(request,
                          "AdminUnit/report_hours_by_time_and_org.html",
                          {"values": data,
                           "selectTimeForm": {},
                              "selectOrgForm": {},
                              "details": details})
        else:
            return render(request,
                          "AdminUnit/report_hours_by_time_and_org.html",
                          {"values": {},
                           "selectTimeForm": selectTimeForm,
                           "selectOrgForm": selectOrgForm,
                           "details": {}})
    else:
        selectTimeForm = SelectTimeForm()
        selectOrgForm = SelectOrgForm()
        data = []
        return render(request,
                      "AdminUnit/report_hours_by_time_and_org.html",
                      {"values": data,
                       "selectTimeForm": selectTimeForm,
                       "selectOrgForm": selectOrgForm,
                       "details": {}})
