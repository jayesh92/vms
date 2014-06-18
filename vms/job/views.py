from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from job.models import Job, Shift
from job.forms import JobForm, ShiftForm
from job.services import *

def index(request):
    return HttpResponseRedirect(reverse('job:list'))

def add_shift(request):

    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        if job_id:
            job = get_job_by_id(job_id)
            if job:
                form = ShiftForm(request.POST)
                if form.is_valid():
                    shift = form.save(commit=False)
                    shift.job = job
                    shift.save()
                    return render(request, 'job/add_shift_success.html')
                else:
                    return HttpResponseRedirect(reverse('job:error'))
            else:
                return HttpResponseRedirect(reverse('job:error'))
        else:
            return HttpResponseRedirect(reverse('job:error'))
    else:
        return HttpResponseRedirect(reverse('job:error'))

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

def create_shift(request):

    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        if job_id:
            form = ShiftForm()
            return render(request, 'job/create_shift.html', {'form' : form, 'job_id' : job_id,})
    else:
        return HttpResponseRedirect(reverse('job:error'))

def details(request):
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        if job_id:
            #retrieve the logged in user.id and from this retrieve the corresponding volunteer.id 
            #for now, use rango to provide authentication and authorization functionality
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
    else:
        return HttpResponseRedirect(reverse('job:error'))

def authorization_error(request):
    return render(request, 'rango/error.html')

def error(request):
    return render(request, 'vms/error.html')

def list(request):
    job_list = get_jobs_by_title()
    return render(request, 'job/sign_up_list.html', {'job_list' : job_list})

def manage(request):
    job_list = get_jobs_by_title()
    return render(request, 'job/add_shift_list.html', {'job_list' : job_list})

def sign_up(request):
    if request.method == 'POST':
        shift_id = request.POST.get('shift_id')
        if shift_id:
            #retrieve the logged in user.id and from this retrieve the corresponding volunteer.id 
            #for now, use rango to provide authentication and authorization functionality
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
            return HttpResponseRedirect(reverse('job:error'))
    else:
        return HttpResponseRedirect(reverse('job:error'))
