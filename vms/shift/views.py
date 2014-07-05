from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from job.models import Job
from job.services import *
from shift.forms import HoursForm, ShiftForm
from shift.models import Shift
from shift.services import *
from volunteer.services import *

def index(request):
    return HttpResponseRedirect(reverse('job:list_jobs'))
    
def add_hours(request, shift_id, volunteer_id):
    if shift_id and volunteer_id:
        if request.method == 'POST':
            form = HoursForm(request.POST)
            if form.is_valid():
                start_time = form.cleaned_data['start_time']
                end_time = form.cleaned_data['end_time']
                result = add_shift_hours(volunteer_id, shift_id, start_time, end_time)
                if result:
                    return render(request, 'shift/add_hours_success.html')
                else:
                    return HttpResponseRedirect(reverse('shift:error'))
            else:
                form = HoursForm()
                return render(request, 'shift/add_hours.html', {'form' : form, 'shift_id' : shift_id, 'volunteer_id' : volunteer_id,})
        else:
            form = HoursForm()
            return render(request, 'shift/add_hours.html', {'form' : form, 'shift_id' : shift_id, 'volunteer_id' : volunteer_id,})
    else:
        return HttpResponseRedirect(reverse('shift:error'))
        
def authorization_error(request):
    return render(request, 'auth/error.html')

def cancel_shift(request, shift_id, volunteer_id):
    if shift_id and volunteer_id:
        if request.method == 'POST':
            result = cancel_shift_registration(volunteer_id, shift_id)
            if result:
                return HttpResponseRedirect(reverse('shift:view_volunteer_shifts', args=(volunteer_id,)))
            else:
                return HttpResponseRedirect(reverse('shift:error'))
        else:            
            return render(request, 'shift/cancel_shift_confirmation.html', {'shift_id' : shift_id, 'volunteer_id' : volunteer_id})
    else:
        return HttpResponseRedirect(reverse('shift:error'))
        
def create_shift(request, job_id):

    if job_id:
        if request.method == 'POST':
            job = get_job_by_id(job_id)
            if job:
                form = ShiftForm(request.POST)
                if form.is_valid():
                    shift = form.save(commit=False)
                    #Keep track of number of open slots
                    shift.slots_remaining = shift.max_volunteers;
                    shift.job = job
                    shift.save()
                    return render(request, 'shift/create_shift_success.html')
                else:
                    form = ShiftForm()
                    return render(request, 'shift/create_shift.html', {'form' : form, 'job_id' : job_id,})
            else:
                return HttpResponseRedirect(reverse('shift:error'))
        else:
            form = ShiftForm()
            return render(request, 'shift/create_shift.html', {'form' : form, 'job_id' : job_id,})
    else:
        return HttpResponseRedirect(reverse('shift:error'))
        
def error(request):
    return render(request, 'vms/error.html')
    
def shift_sign_up(request, shift_id):
    if shift_id:
        if request.method == 'POST':
            #retrieve the logged in user.id and from this retrieve the corresponding volunteer.id 
            #for now, use auth app to provide authentication and authorization functionality
            user = request.user
            if user.is_authenticated():
                volunteer_id = user.volunteer.id
                result = register(volunteer_id, shift_id)
                if result:
                    return render(request, 'shift/sign_up_success.html')
                else:
                    return render(request, 'shift/sign_up_error.html')
            else:
                return HttpResponseRedirect(reverse('shift:authorization_error'))
        else:
            return render(request, 'shift/sign_up_confirmation.html', {'shift_id' : shift_id,})
    else:
        return HttpResponseRedirect(reverse('shift:error'))

def view_hours(request, shift_id, volunteer_id):
    if shift_id and volunteer_id:
        volunteer_shift = get_volunteer_shift_by_id(volunteer_id, shift_id)
        if volunteer_shift:
            #need to first check that the volunteer entered hours first
            working_duration = "{0:.2f}".format(calculate_working_duration(volunteer_shift.start_time, volunteer_shift.end_time))
            return render(request, 'shift/hours_list.html', {'volunteer_shift' : volunteer_shift, 'working_duration' : working_duration,})
        else:
            return HttpResponseRedirect(reverse('shift:error'))
    else:
        return HttpResponseRedirect(reverse('shift:error'))

def view_volunteer_shifts(request, volunteer_id):
    if volunteer_id:
        volunteer = get_volunteer_by_id(volunteer_id)
        if volunteer:
            shift_list = get_shifts_signed_up_for(volunteer_id)
            return render(request, 'shift/volunteer_shifts.html', {'shift_list' : shift_list, 'volunteer_id' : volunteer_id,})
        else:
            return HttpResponseRedirect(reverse('shift:error'))
    else:
        return HttpResponseRedirect(reverse('shift:error'))                    
