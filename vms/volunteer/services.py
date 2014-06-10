from django.core.exceptions import ObjectDoesNotExist
from volunteer.models import Volunteer

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

def has_resume_file(volunteer_id):
    
    result = False 
    volunteer = get_volunteer_by_id(volunteer_id)

    if volunteer and volunteer.resume_file:
        result = True 

    return result
    
def get_volunteer_resume_file_url(volunteer_id):

    result = None
    volunteer = get_volunteer_by_id(volunteer_id)

    if volunteer and volunteer.resume_file:
        result = volunteer.resume_file.url

    return result 

def get_volunteers_by_first_name():
    volunteer_list = Volunteer.objects.all().order_by('first_name')
    return volunteer_list

#delete any corresponding resumes
def delete_volunteer(volunteer_id):
    volunteer = get_volunteer_by_id(volunteer_id)
    if volunteer:
        volunteer.delete()
    else:
        print "return some error here"

def delete_volunteer_resume(volunteer_id):

    result = False 
    volunteer = get_volunteer_by_id(volunteer_id)

    if volunteer and volunteer.resume_file:
        volunteer.resume_file.delete()
        result = True

    return result


def search_volunteers(first_name, last_name, city, state, country, company):
    
    #if no search parameters are given, it returns all volunteers
    search_query = Volunteer.objects.all()

    #build query based on parameters provided
    if first_name:
        search_query =  search_query.filter(first_name__icontains=first_name)
    if last_name:
        search_query = search_query.filter(last_name__icontains=last_name)
    if city:
        search_query = search_query.filter(city__icontains=city)
    if state:
        search_query = search_query.filter(state__icontains=state)
    if country:
        search_query = search_query.filter(country__icontains=country)
    if company:
        search_query = search_query.filter(company__icontains=company)

    return search_query 
