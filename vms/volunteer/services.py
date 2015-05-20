from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from organization.services import *
from volunteer.models import Volunteer

def delete_volunteer(volunteer_id):

    volunteer = get_volunteer_by_id(volunteer_id)

    if volunteer:
        #if the volunteer uploaded a resume, delete it as well
        if has_resume_file(volunteer_id):
            delete_volunteer_resume(volunteer_id)
        #Django docs recommend to set associated user to not active instead of deleting the user
        user = volunteer.user
        user.is_active = False
        #make a call to update the user
        user.save()
        #then delete the volunteer
        volunteer.delete()
    else:
        return ObjectDoesNotExist

def delete_volunteer_resume(volunteer_id):

    volunteer = get_volunteer_by_id(volunteer_id)

    if volunteer and volunteer.resume_file:
        volunteer.resume_file.delete()
    else:
        return ObjectDoesNotExist

def get_all_volunteers():
    
    volunteer_list = Volunteer.objects.all()
    return volunteer_list

def get_volunteer_by_id(volunteer_id):

    is_valid = True
    result = None

    try:
        volunteer = Volunteer.objects.get(pk=volunteer_id)
    except ObjectDoesNotExist:  
        is_valid = False
        
    if is_valid:
        result = volunteer

    return result  

def get_volunteer_resume_file_url(volunteer_id):

    result = None
    volunteer = get_volunteer_by_id(volunteer_id)

    if volunteer and volunteer.resume_file:
        result = volunteer.resume_file.url

    return result 

def get_volunteers_ordered_by_first_name():
    volunteer_list = Volunteer.objects.all().order_by('first_name')
    return volunteer_list

def has_resume_file(volunteer_id):
    
    result = False 
    volunteer = get_volunteer_by_id(volunteer_id)

    if volunteer and volunteer.resume_file:
        result = True 

    return result

def search_volunteers(first_name, last_name, city, state, country, organization):
    
    #if no search parameters are given, it returns all volunteers
    search_query = Volunteer.objects.all()

    #build query based on parameters provided
    if first_name:
        search_query = search_query.filter(first_name__icontains=first_name)
    if last_name:
        search_query = search_query.filter(last_name__icontains=last_name)
    if city:
        search_query = search_query.filter(city__icontains=city)
    if state:
        search_query = search_query.filter(state__icontains=state)
    if country:
        search_query = search_query.filter(country__icontains=country)
    if organization:
        organization_obj = get_organization_by_name(organization)
        organization_list = get_organizations_ordered_by_name()
        if organization_obj in organization_list:
            #organization associated with a volunteer can be null
            #therefore exclude from the search query volunteers with no associated organization
            #then filter by organization_name
            search_query = search_query.exclude(organization__isnull=True).filter(organization__name__icontains=organization)
        else:
            #unlisted_organization associated with a volunteer can be left blank
            #therefore exclude from the search query volunteers with a blank unlisted_organization
            #then filter by the unlisted organization name
            search_query = search_query.exclude(unlisted_organization__exact='').filter(unlisted_organization__icontains=organization)

    return search_query 
