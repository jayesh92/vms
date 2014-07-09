from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from organization.forms import OrganizationForm

def index(request):
    return HttpResponseRedirect(reverse('organization:create'))

def create(request):
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'organization/create_success.html') 
        else:
            return render(request, 'organization/create.html', {'form' : form,})
    else:
        form = OrganizationForm()
        return render(request, 'organization/create.html', {'form' : form,})

def error(request):
    return render(request, 'organization/error.html')
