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

def register(_volunteer_id, _job_id):

    is_valid = True
    is_already_registered = True

    #a volunteer must not be allowed to register for a job that they are already registered for
    try:
        registration_obj = VolunteerJob.objects.get(volunteer_id=_volunteer_id, job_id=_job_id)
    except ObjectDoesNotExist:
        is_already_registered = False

    if not is_already_registered:
        _volunteer = get_volunteer_by_id(_volunteer_id)
        _job = get_job_by_id(_job_id) 

        if _volunteer and _job:
            registration_obj = VolunteerJob(volunteer=_volunteer, job=_job)
            registration_obj.save()
        else:
            is_valid = False
    else:
        is_valid = False

    return is_valid
