from django.core.exceptions import ObjectDoesNotExist
from job.models import Job, VolunteerJob
from volunteer.services import get_volunteer_by_id

def get_job_by_id(job_id):

    is_valid = True
    result = None

    try:
        job = Job.objects.get(pk=job_id)
    except ObjectDoesNotExist:
        is_valid = False

    if is_valid:
        result = job

    return result

def get_jobs_by_title():
    job_list = Job.objects.all().order_by('job_title')
    return job_list

def is_signed_up(v_id, j_id):

    result = True
    
    try:
        obj = VolunteerJob.objects.get(volunteer_id=v_id, job_id=j_id)
    except ObjectDoesNotExist:
        result = False          

    return result

def register(v_id, j_id):

    is_valid = True

    #a volunteer must not be allowed to register for a job that they are already registered for
    signed_up = is_signed_up(v_id, j_id)

    if not signed_up:
        volunteer_obj = get_volunteer_by_id(v_id)
        job_obj = get_job_by_id(j_id) 

        if volunteer_obj and job_obj:
            registration_obj = VolunteerJob(volunteer=volunteer_obj, job=job_obj)
            registration_obj.save()
        else:
            is_valid = False
    else:
        is_valid = False

    return is_valid
