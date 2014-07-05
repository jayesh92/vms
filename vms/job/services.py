import datetime
from django.core.exceptions import ObjectDoesNotExist
from job.models import Job

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
