from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from job.models import Job, Shift
from job.forms import JobForm, ShiftForm
from job.services import *
from volunteer.services import *

def index(request):
    return HttpResponseRedirect(reverse('job:list_jobs'))

def authorization_error(request):
    return render(request, 'auth/error.html')

def cancel_shift(request, shift_id, volunteer_id):
    if shift_id and volunteer_id:
        if request.method == 'POST':
            result = cancel_shift_registration(shift_id, volunteer_id)
            if result:
                return HttpResponseRedirect(reverse('job:view_volunteer_shifts', args=(volunteer_id,)))
            else:
                return HttpResponseRedirect(reverse('job:error'))
        else:            
            return render(request, 'job/cancel_shift_confirmation.html', {'shift_id' : shift_id, 'volunteer_id' : volunteer_id})
    else:
        return HttpResponseRedirect(reverse('job:error'))

def create_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('job:manage_jobs'))
        else:
            return render(request, 'job/create_job.html', {'form' : form,})
    else:
        form = JobForm()
        return render(request, 'job/create_job.html', {'form' : form,})

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
                    return render(request, 'job/create_shift_success.html')
                else:
                    return HttpResponseRedirect(reverse('job:error'))
            else:
                return HttpResponseRedirect(reverse('job:error'))
        else:
            form = ShiftForm()
            return render(request, 'job/create_shift.html', {'form' : form, 'job_id' : job_id,})
    else:
        return HttpResponseRedirect(reverse('job:error'))

def details(request, job_id):
    #it's fine to do the following processing after a GET request because we are just retrieving
    #and not setting any data here
    if job_id:
        #retrieve the logged in user.id and from this retrieve the corresponding volunteer.id 
        #for now, use auth app to provide authentication and authorization functionality
        user = request.user
        if user.is_authenticated():
            volunteer_id = user.volunteer.id
            job = get_job_by_id(job_id)
            shift_list = get_shifts_by_date(job_id)
            signed_up_list = get_shifts_signed_up_for(volunteer_id)
            if job:
                return render(request, 'job/details.html', {'job' : job, 'shift_list' : shift_list, 'signed_up_list' : signed_up_list,})
            else:
                return HttpResponseRedirect(reverse('job:error'))
        else:
            return HttpResponseRedirect(reverse('job:authorization_error'))
    else:
        return HttpResponseRedirect(reverse('job:error'))

def error(request):
    return render(request, 'vms/error.html')

def list_jobs(request):
    job_list = get_jobs_by_title()
    return render(request, 'job/job_list.html', {'job_list' : job_list})

def manage_jobs(request):
    job_list = get_jobs_by_title()
    return render(request, 'job/manage_job_list.html', {'job_list' : job_list})

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
                    return render(request, 'job/sign_up_success.html')
                else:
                    return render(request, 'job/sign_up_error.html')
            else:
                return HttpResponseRedirect(reverse('job:authorization_error'))
        else:
            return render(request, 'job/sign_up_confirmation.html', {'shift_id' : shift_id,})
    else:
        return HttpResponseRedirect(reverse('job:error'))

def view_volunteer_shifts(request, volunteer_id):
    if volunteer_id:
        volunteer = get_volunteer_by_id(volunteer_id)
        if volunteer:
            shift_list = get_shifts_signed_up_for(volunteer_id)
            return render(request, 'job/volunteer_shifts.html', {'shift_list' : shift_list, 'volunteer_id' : volunteer_id,})
        else:
            return HttpResponseRedirect(reverse('job:error'))
    else:
        return HttpResponseRedirect(reverse('job:error'))
