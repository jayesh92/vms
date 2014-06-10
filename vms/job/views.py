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

def list_jobs(request):
    job_list = get_jobs_by_title()
    return render(request, 'job/list.html', {'job_list' : job_list})
