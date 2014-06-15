from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from job.models import Job
from job.forms import JobForm
from job.services import *

def index(request):
    return HttpResponseRedirect(reverse('job:list'))

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
            return HttpResponseRedirect(reverse('job:list'))
        else:
            return render(request, 'job/create.html', {'form' : form,})
    else:
        form = JobForm()
        return render(request, 'job/create.html', {'form' : form,})

def details(request):
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        if job_id:
            #retrieve the logged in user.id and from this retrieve the corresponding volunteer.id 
            #for now, use rango to provide authentication and authorization functionality
            user = request.user
            if user.is_authenticated():
                volunteer_id = user.volunteer.id
                signed_up = is_signed_up(volunteer_id, job_id)
                job = get_job_by_id(job_id)
                if job:
                    return render(request, 'job/details.html', {'job' : job, 'signed_up' : signed_up})
                else:
                    return HttpResponseRedirect(reverse('job:error'))
            else:
                return HttpResponseRedirect(reverse('job:authorization_error'))
        else:
            return HttpResponseRedirect(reverse('job:error'))
    else:
        return HttpResponseRedirect(reverse('job:error'))

def authorization_error(request):
    return render(request, 'rango/error.html')

def error(request):
    return render(request, 'vms/error.html')

def list(request):
    job_list = get_jobs_by_title()
    return render(request, 'job/list.html', {'job_list' : job_list})

def sign_up(request):
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        if job_id:
            #retrieve the logged in user.id and from this retrieve the corresponding volunteer.id 
            #for now, use rango to provide authentication and authorization functionality
            user = request.user
            if user.is_authenticated():
                volunteer_id = user.volunteer.id
                result = register(volunteer_id, job_id)
                if result:
                    return render(request, 'job/sign_up_success.html')
                else:
                    return render(request, 'job/sign_up_error.html')
            else:
                return HttpResponseRedirect(reverse('job:authorization_error'))
        else:
            return HttpResponseRedirect(reverse('job:error'))
    else:
        return HttpResponseRedirect(reverse('job:error'))
