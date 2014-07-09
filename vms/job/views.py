from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from job.models import Job
from job.forms import JobForm
from job.services import *
from shift.models import Shift
from shift.services import *
from volunteer.services import *

def index(request):
    return HttpResponseRedirect(reverse('job:list_jobs'))
    
def authorization_error(request):
    return render(request, 'auth/error.html')
    
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
