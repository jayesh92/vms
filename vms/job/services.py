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

def register(volunteer_id, job_id):

    is_valid = True

    _volunteer = get_volunteer_by_id(volunteer_id)
    _job = get_job_by_id(job_id) 

    if _volunteer and _job:
        volunteer_job = VolunteerJob(volunteer=_volunteer, job=_job)
        volunteer_job.save()
    else:
        is_valid = False

    return is_valid
