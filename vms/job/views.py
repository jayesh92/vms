from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from job.models import Job
from job.forms import JobForm
from job.services import *

# Create your views here.
def index(request):
    return HttpResponseRedirect(reverse('job:list_jobs'))

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

def error(request):
    return render(request, 'job/error.html')

def list_jobs(request):
    job_list = get_jobs_by_title()
    return render(request, 'job/list.html', {'job_list' : job_list})

def confirmation(request):
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        if job_id:
            return render(request, 'job/confirmation.html', {'id' : job_id,})
        else:
            return HttpResponseRedirect(reverse('job:error'))
    else:
        return HttpResponseRedirect(reverse('job:error'))

def sign_up(request):
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        if job_id:
            #retrieve the logged in user.id and from this retrieve the corresponding volunteer.id 
            #we cannot do this right now because I do not have Jayesh's authentication code
            #use a test value for now
            volunteer_id = 1
            result = register(volunteer_id, job_id)
            if result:
                return render(request, 'job/message.html')
            else:
                return HttpResponseRedirect(reverse('job:error'))
        else:
            return HttpResponseRedirect(reverse('job:error'))
    else:
        return HttpResponseRedirect(reverse('job:error'))

