import os
from django.conf import settings
from django.contrib.auth.models import User
from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from volunteer.forms import SearchVolunteerForm, VolunteerForm
from volunteer.models import Volunteer
from volunteer.services import * 
from volunteer.validation import *

def index(request):
    return HttpResponseRedirect(reverse('volunteer:create'))

def create(request):
    if request.method == 'POST':
        form = VolunteerForm(request.POST, request.FILES)
        if form.is_valid():
            #if a resume has been uploaded
            if 'resume_file' in request.FILES:
                my_file = form.cleaned_data['resume_file']
                if not validate_file(my_file):
                    return render(request, 'volunteer/create.html', {'form' : form,})        
            #save the volunteer
            form.save()
            return HttpResponseRedirect(reverse('volunteer:list'))
        else:
            return render(request, 'volunteer/create.html', {'form' : form,})        
    else:
        form = VolunteerForm()
        return render(request, 'volunteer/create.html', {'form' : form,})        

def download_resume(request, volunteer_id):
    if request.method == 'POST':
        basename = get_volunteer_resume_file_url(volunteer_id)
        if basename:
            filename = settings.MEDIA_ROOT + basename 
            wrapper = FileWrapper(file(filename))
            response = HttpResponse(wrapper)
            response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filename)
            response['Content-Length'] = os.path.getsize(filename)
            return response
        else:
            return HttpResponseRedirect(reverse('volunteer:error'))
    else:
        return HttpResponseRedirect(reverse('volunteer:error'))

def delete(request, volunteer_id):
    if request.method == 'POST':
        #any type of deletion should be done on a POST (not a GET)
        result = delete_volunteer(volunteer_id)
        if result:
            return HttpResponseRedirect(reverse('volunteer:list'))
        else:
            return HttpResponseRedirect(reverse('volunteer:error'))
    else:
        return render(request, 'volunteer/delete.html', {'id' : volunteer_id,})

def delete_resume(request, volunteer_id):
    if request.method == 'POST':
        if delete_volunteer_resume(volunteer_id):
            return HttpResponseRedirect(reverse('volunteer:list'))
        else:
            return HttpResponseRedirect(reverse('volunteer:error'))
    else:
        return HttpResponseRedirect(reverse('volunteer:error'))

def edit(request, volunteer_id):
    #check that volunteer_id is valid since we may potentially have to pass it back to the template
    volunteer = get_volunteer_by_id(volunteer_id)
    if volunteer:
        if request.method == 'POST':
            form = VolunteerForm(request.POST, request.FILES, instance=volunteer)
            if form.is_valid():
                #if a resume has been uploaded
                if 'resume_file' in request.FILES:
                    my_file = form.cleaned_data['resume_file']
                    if validate_file(my_file):
                        #delete an old uploaded resume if it exists
                        has_file = has_resume_file(volunteer_id)
                        if has_file:
                            if not delete_volunteer_resume(volunteer_id):
                                return HttpResponseRedirect(reverse('volunteer:error'))
                    else:
                        return render(request, 'volunteer/edit.html', {'form' : form, 'id' : volunteer_id,})
                #update the volunteer
                form.save()
                return HttpResponseRedirect(reverse('volunteer:list'))
            else:
                return render(request, 'volunteer/edit.html', {'form' : form, 'id' : volunteer_id,})
        else:
            #create a form to change an existing volunteer
            form = VolunteerForm(instance=volunteer)
            return render(request, 'volunteer/edit.html', {'form' : form, 'id' : volunteer_id,})
    else:
        return HttpResponseRedirect(reverse('volunteer:error'))

def error(request):
    return render(request, 'vms/error.html')

def options(request):
    if request.method == 'POST':

        option = request.POST.get('option')
        volunteer_id = request.POST.get('volunteer_id')
        
        if option and volunteer_id:
            volunteer = get_volunteer_by_id(volunteer_id)
            if volunteer:
                if option == 'profile':
                    return HttpResponseRedirect(reverse('volunteer:profile', args=(volunteer_id,)))
                elif option == 'edit':
                    return HttpResponseRedirect(reverse('volunteer:edit', args=(volunteer_id,))) 
                elif option == 'delete':
                    return HttpResponseRedirect(reverse('volunteer:delete', args=(volunteer_id,)))
                else:
                    return HttpResponseRedirect(reverse('volunteer:error'))
            else:
                return HttpResponseRedirect(reverse('volunteer:error'))
        else:
            return HttpResponseRedirect(reverse('volunteer:error'))
            
def list(request):
    volunteer_list = get_volunteers_by_first_name() 
    return render(request, 'volunteer/list.html', {'volunteer_list' : volunteer_list})

def profile(request, volunteer_id):
    volunteer = get_volunteer_by_id(volunteer_id)
    if volunteer:
        return render(request, 'volunteer/profile.html', {'volunteer' : volunteer})
    else:
        return HttpResponseRedirect(reverse('volunteer:error'))

def search(request):
    if request.method == 'POST':
        form = SearchVolunteerForm(request.POST)
        if form.is_valid():

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            country = form.cleaned_data['country']
            company = form.cleaned_data['company']

            search_result_list = search_volunteers(first_name, last_name, city, state, country, company)
            return render(request, 'volunteer/search_result.html', {'search_result_list' : search_result_list})
    else:
        form = SearchVolunteerForm()

    return render(request, 'volunteer/search.html', {'form' : form})
