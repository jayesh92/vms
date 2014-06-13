from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from job.models import Job
from job.forms import JobForm
from job.services import *

def index(request):
    return HttpResponseRedirect(reverse('job:list_jobs'))

def confirmation(request):
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        if job_id:
            return render(request, 'job/confirmation.html', {'id' : job_id,})
        else:
            return HttpResponseRedirect(reverse('job:error'))
    else:
        return HttpResponseRedirect(reverse('job:error'))

def create(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('job:list_jobs'))
        else:
            return render(request, 'job/create.html', {'form' : form,})
    else:
        form = JobForm()
        return render(request, 'job/create.html', {'form' : form,})

def details(request):
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        if job_id:
            #use a test value for now
            volunteer_id = 10
            signed_up = is_signed_up(volunteer_id, job_id)
            job = get_job_by_id(job_id)
            if job:
                return render(request, 'job/details.html', {'job' : job, 'signed_up' : signed_up})
            else:
                return render(request, 'job/error.html')
        else:
            return render(request, 'job/error.html')
    else:
        return render(request, 'job/error.html')

def error(request):
    return render(request, 'job/error.html')

def list_jobs(request):
    job_list = get_jobs_by_title()
    return render(request, 'job/list.html', {'job_list' : job_list})

def sign_up(request):
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        if job_id:
            #retrieve the logged in user.id and from this retrieve the corresponding volunteer.id 
            #we cannot do this right now because I do not have Jayesh's authentication code
            #use a test value for now
            volunteer_id = 10
            result = register(volunteer_id, job_id)
            if result:
                return render(request, 'job/message.html')
            else:
                return render(request, 'job/error_code.html')
        else:
            return HttpResponseRedirect(reverse('job:error'))
    else:
        return HttpResponseRedirect(reverse('job:error'))

