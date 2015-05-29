import os
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from organization.services import *
from shift.services import *
from volunteer.forms import ReportForm, SearchVolunteerForm, VolunteerForm
from volunteer.models import Volunteer
from volunteer.services import * 
from volunteer.validation import validate_file

@login_required
def download_resume(request, volunteer_id):
    user = request.user
    if int(user.volunteer.id) == int(volunteer_id):
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
                raise Http404
    else:
        return HttpResponse(status=403)
        
@login_required
def delete_resume(request, volunteer_id):
    user = request.user
    if int(user.volunteer.id) == int(volunteer_id):
        if request.method == 'POST':
            try:
                delete_volunteer_resume(volunteer_id)
                return HttpResponseRedirect(reverse('volunteer:profile', args=(volunteer_id,)))
            except:
                raise Http404
    else:
        return HttpResponse(status=403)  

@login_required
def edit(request, volunteer_id):

    volunteer = get_volunteer_by_id(volunteer_id)
    if volunteer:
        user = request.user
        if int(user.volunteer.id) == int(volunteer_id):
            organization_list = get_organizations_ordered_by_name()
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
                                try:
                                    delete_volunteer_resume(volunteer_id)
                                except:
                                    raise Http404
                        else:
                            return render(request, 'volunteer/edit.html', {'form' : form, 'organization_list' : organization_list, 'volunteer' : volunteer, 'resume_invalid' : True,})
                    
                    volunteer_to_edit = form.save(commit=False)

                    organization_id = request.POST.get('organization_name')
                    organization = get_organization_by_id(organization_id)
                    if organization:
                        volunteer_to_edit.organization = organization
                    else:
                        volunteer_to_edit.organization = None

                    #update the volunteer
                    volunteer_to_edit.save()
                    return HttpResponseRedirect(reverse('volunteer:profile', args=(volunteer_id,)))
                else:
                    print form.errors
                    return render(request, 'volunteer/edit.html', {'form' : form, 'organization_list' : organization_list, 'volunteer' : volunteer,})
            else:
                #create a form to change an existing volunteer
                form = VolunteerForm(instance=volunteer)
                return render(request, 'volunteer/edit.html', {'form' : form, 'organization_list' : organization_list, 'volunteer' : volunteer,})
        else:
            return HttpResponse(status=403)
    else:
        raise Http404
        
@login_required
def profile(request, volunteer_id):

    volunteer = get_volunteer_by_id(volunteer_id)
    if volunteer:
        user = request.user
        if int(user.volunteer.id) == int(volunteer_id):
            return render(request, 'volunteer/profile.html', {'volunteer' : volunteer})
        else:
            return HttpResponse(status=403)
    else:
        #if Http404 is raised at any point in a view function, Django will catch it and return the standard
        #error page, along with an HTTP error code 404
        raise Http404

@login_required
def report(request, volunteer_id):
    volunteer = get_volunteer_by_id(volunteer_id)
    if volunteer:
        user = request.user
        if int(user.volunteer.id) == int(volunteer_id):
            if request.method == 'POST':
                form = ReportForm(request.POST)
                if form.is_valid():
                    event_name = form.cleaned_data['event_name']
                    job_name = form.cleaned_data['job_name']
                    date = form.cleaned_data['date']
                    report_list = get_volunteer_report(volunteer_id, event_name, job_name, date)
                    total_hours = calculate_total_report_hours(report_list)
                    return render(request, 'volunteer/report.html', {'form' : form, 'report_list' : report_list, 'total_hours' : total_hours, 'notification' : True})
                else:
                    return render(request, 'volunteer/report.html', {'form' : form, 'notification' : False})
            else:
                form = ReportForm()
                return render(request, 'volunteer/report.html', {'form' : form, 'notification' : False})
        else:
            return HttpResponse(status=403)
    else:
        raise Http404

@login_required
def search(request):
    if request.method == 'POST':
        form = SearchVolunteerForm(request.POST)
        if form.is_valid():

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            country = form.cleaned_data['country']
            organization = form.cleaned_data['organization']

            search_result_list = search_volunteers(first_name, last_name, city, state, country, organization)
            return render(request, 'volunteer/search.html', {'form' : form, 'has_searched' : True, 'search_result_list' : search_result_list})
    else:
        form = SearchVolunteerForm()

    return render(request, 'volunteer/search.html', {'form' : form, 'has_searched' : False})
