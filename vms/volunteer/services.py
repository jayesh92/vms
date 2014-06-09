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

def get_volunteer_resume_file(volunteer_id):
    volunteer = get_volunteer_by_id(volunteer_id)
    resume_file = volunteer.resume_file
    return resume_file
    
def get_volunteer_resume_file_url(volunteer_id):
    volunteer = get_volunteer_by_id(volunteer_id)
    path = volunteer.resume_file.url
    return path

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
    volunteer = get_volunteer_by_id(volunteer_id)
    volunteer.resume_file.delete()

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

def validate_file(my_file):
    MAX_FILENAME_LENGTH = 40
    MAX_FILESIZE_BYTES = 5243000
    VALID_CONTENT_TYPES = [
        "application/pdf", 
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.oasis.opendocument.text"
    ]

    is_valid = True

    if len(my_file.name) > MAX_FILENAME_LENGTH:
        is_valid = False
    if my_file.size > MAX_FILESIZE_BYTES:
        is_valid = False
    if my_file.content_type not in VALID_CONTENT_TYPES:
        is_valid = False
           
    return is_valid
