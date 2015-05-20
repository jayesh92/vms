import datetime
from django.core.exceptions import ObjectDoesNotExist
from job.models import Job

def delete_job(job_id):

    result = True
    job = get_job_by_id(job_id)
    shifts_in_job = job.shift_set.all()

    if job and (not shifts_in_job):
        job.delete()
    else:
        result = False

    return result

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

def get_jobs_by_event_id(e_id):
    job_list = Job.objects.filter(event_id=e_id)
    return job_list

def get_jobs_ordered_by_title():
    job_list = Job.objects.all().order_by('name')
    return job_list
