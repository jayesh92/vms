from administrator.forms import AdministratorForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from organization.services import *
from registration.forms import UserForm
from volunteer.forms import VolunteerForm
from volunteer.models import Volunteer #Volunteer model needs to be imported so that input type file renders properly
from volunteer.validation import validate_file

def signup_administrator(request):
    """
    This method is responsible for diplaying the register user view
    Register Admin or volunteer is judged on the basis of users 
    access rights.
    Only if user is registered and logged in and registered as an
    admin user, he/she is allowed to register others as an admin user
    """
    registered = False
    organization_list = get_organizations_ordered_by_name()
    
    if organization_list:
        #if request.user.username != '' and request.user.is_authenticated(
        #) and checkAdmin(request.user):
        if request.method == 'POST':
            user_form = UserForm(request.POST, prefix="usr")
            administrator_form = AdministratorForm(request.POST, prefix="admin")

            if user_form.is_valid() and administrator_form.is_valid():
                user = user_form.save();
                user.set_password(user.password)
                user.save()
                
                administrator = administrator_form.save(commit=False)
                administrator.user = user
                
                #if organization isn't chosen from dropdown, the organization_id will be 0
                organization_id = request.POST.get('organization_name')
                organization = get_organization_by_id(organization_id)
                
                if organization:
                    administrator.organization = organization
                    
                administrator.save()
                registered = True

                return HttpResponseRedirect(reverse('home:index'))
            else:
                print user_form.errors, administrator_form.errors
                return render(request, 'registration/signup_administrator.html', {'user_form' : user_form, 'administrator_form' : administrator_form, 'registered' : registered, 'organization_list' : organization_list,})
        else:
            user_form = UserForm(prefix="usr")
            administrator_form = AdministratorForm(prefix="admin")
                       
        return render(request, 'registration/signup_administrator.html', {'user_form' : user_form, 'administrator_form' : administrator_form, 'registered' : registered, 'organization_list' : organization_list,})

    else:
        return render(request, 'organization/add_organizations.html')

def signup_volunteer(request):

    registered = False
    organization_list = get_organizations_ordered_by_name()

    if organization_list:
        if request.method == 'POST':
            #each form must have it's own namespace (prefix) if multiple forms are to be put inside one <form> tag
            user_form = UserForm(request.POST, prefix="usr")
            volunteer_form = VolunteerForm(request.POST, request.FILES, prefix="vol")

            if user_form.is_valid() and volunteer_form.is_valid():

                if 'resume_file' in request.FILES:
                    my_file = volunteer_form.cleaned_data['resume_file']
                    if not validate_file(my_file):
                        return render(request, 'registration/signup_volunteer.html', {'user_form' : user_form, 'volunteer_form' : volunteer_form, 'registered' : registered, 'organization_list' : organization_list,})

                user = user_form.save();

                user.set_password(user.password)
                user.save()
           
                volunteer = volunteer_form.save(commit=False)
                volunteer.user = user

                #if an organization isn't chosen from the dropdown, then organization_id will be 0
                organization_id = request.POST.get('organization_name')
                organization = get_organization_by_id(organization_id)

                if organization:
                    volunteer.organization = organization

                volunteer.save()
                registered = True

                return HttpResponseRedirect(reverse('home:index'))
            else:
                print user_form.errors, volunteer_form.errors
                return render(request, 'registration/signup_volunteer.html', {'user_form' : user_form, 'volunteer_form' : volunteer_form, 'registered' : registered, 'organization_list' : organization_list,})
        else:
            user_form = UserForm(prefix="usr")
            volunteer_form = VolunteerForm(prefix="vol") 

        return render(request, 'registration/signup_volunteer.html', {'user_form' : user_form, 'volunteer_form' : volunteer_form, 'registered' : registered, 'organization_list' : organization_list,})

    else:
        return render(request, 'organization/add_organizations.html')
