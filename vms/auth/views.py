from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from organization.services import *
from auth.forms import UserForm, UserProfileForm
from volunteer.forms import VolunteerForm
from volunteer.models import Volunteer #Volunteer model needs to be imported so that input type file renders properly
from volunteer.validation import validate_file

def register(request):

    registered = False
    if request.method == 'POST':

        #grab info from raw form information
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            #save form data to database
            user = user_form.save();

            #hash password with the set password method
            user.set_password(user.password)
            user.save()

            #we need to set user attribute ourselves, we set 
            #commit=False. This delays saving the model until
            #we're ready to avoid integrity problems
            profile = profile_form.save(commit=False)

            #reference the User model to the UserProfile instance
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            
            registered = True            
        else:
            print user_form.errors, profile_form.errors

    else:
        #render unbound forms
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(
        request,
        'auth/register.html',
        {'user_form': user_form, 'profile_form' : profile_form, 'registered' : registered,}
    )

def register_volunteer(request):

    registered = False
    organization_list = get_organizations_by_name()

    if request.method == 'POST':

        #each form must have it's own namespace (prefix) if multiple forms are to be put inside one <form> tag
        user_form = UserForm(request.POST, prefix="usr")
        volunteer_form = VolunteerForm(request.POST, request.FILES, prefix="vol")

        if user_form.is_valid() and volunteer_form.is_valid():

            if 'resume_file' in request.FILES:
                my_file = volunteer_form.cleaned_data['resume_file']
                if not validate_file(my_file):
                    return render(
                        request,
                        'auth/register.html',
                        {'user_form' : user_form, 'volunteer_form' : volunteer_form, 'registered' : registered, 'organization_list' : organization_list,}
                    )

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
        else:
            print user_form.errors, volunteer_form.errors
    else:
        user_form = UserForm(prefix="usr")
        volunteer_form = VolunteerForm(prefix="vol") 

    return render(
        request,
        'auth/register.html',
        {'user_form' : user_form, 'volunteer_form' : volunteer_form, 'registered' : registered, 'organization_list' : organization_list,}
    )
    
def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect(reverse('auth:index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'auth/login.html')       


def index(request):
    return render(request, 'auth/index.html')

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

#use the login_required() decorator to ensure only those logged in can access the view
@login_required
def user_logout(request):
    #since the user is logged in, we can now just log them out
    #a call to logout will clean out all the session data for the current request
    logout(request)

    #take the user back to login page
    return HttpResponseRedirect(reverse('auth:user_login'))
