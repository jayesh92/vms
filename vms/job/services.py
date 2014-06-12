from job.models import Job

def get_jobs_by_title():
    job_list = Job.objects.all().order_by('job_title')
    return job_list

def sign_up():
    print "do something"
    
