from django.core.exceptions import ObjectDoesNotExist
from job.models import Job, Shift, VolunteerShift
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

def get_shift_by_id(shift_id):
    
    is_valid = True
    result = None

    try:
        shift = Shift.objects.get(pk=shift_id)
    except ObjectDoesNotExist:
        is_valid = False

    if is_valid:
        result = shift

    return result

def get_shifts_by_date(j_id):
    shift_list = Shift.objects.filter(job_id=j_id).order_by('date')
    return shift_list

def is_signed_up(v_id, s_id):

    result = True
    
    try:
        obj = VolunteerShift.objects.get(volunteer_id=v_id, shift_id=s_id)
    except ObjectDoesNotExist:
        result = False          

    return result

def register(v_id, s_id):

    is_valid = True

    #a volunteer must not be allowed to register for a shift that they are already registered for
    signed_up = is_signed_up(v_id, s_id)

    if not signed_up:
        volunteer_obj = get_volunteer_by_id(v_id)
        shift_obj = get_shift_by_id(s_id) 

        if volunteer_obj and shift_obj:
            registration_obj = VolunteerShift(volunteer=volunteer_obj, shift=shift_obj, hours_worked=0)
            registration_obj.save()
        else:
            is_valid = False
    else:
        is_valid = False

    return is_valid
