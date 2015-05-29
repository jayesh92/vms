from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from organization.forms import OrganizationForm
from organization.services import *

@login_required
def create(request):
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('organization:list'))
        else:
            return render(request, 'organization/create.html', {'form' : form,})
    else:
        form = OrganizationForm()
        return render(request, 'organization/create.html', {'form' : form,})

@login_required
def delete(request, organization_id):

    if request.method == 'POST':
        result = delete_organization(organization_id)
        if result:
            return HttpResponseRedirect(reverse('organization:list'))
        else:
            return render(request, 'organization/delete_error.html')
    return render(request, 'organization/delete.html', {'organization_id' : organization_id})

@login_required
def edit(request, organization_id):

    organization = None
    if organization_id:
        organization = get_organization_by_id(organization_id)

    if request.method == 'POST':
        form = OrganizationForm(request.POST, instance=organization)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('organization:list'))
        else:
            return render(request, 'organization/edit.html', {'form' : form,})
    else:
        form = OrganizationForm(instance=organization)
        return render(request, 'organization/edit.html', {'form' : form,})
        
@login_required
def list(request):
    organization_list = get_organizations_ordered_by_name()
    return render(request, 'organization/list.html', {'organization_list' : organization_list})
