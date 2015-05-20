from django.contrib.auth.models import User
from django.test import TestCase
from event.models import Event
from job.models import Job
from job.services import *
from volunteer.models import Volunteer
from volunteer.services import *

class JobMethodTests(TestCase):

    def test_get_job_by_id(self):

        e1 = Event(name = "Software Conference",
                start_date = "2012-10-22",
                end_date = "2012-10-25")

        e1.save()

        j1 = Job(name = "Software Developer",
                start_date = "2012-10-22",
                end_date = "2012-10-23",
                description = "A software job",
                event = e1)

        j2 = Job(name = "Systems Administrator",
                start_date = "2012-9-1",
                end_date = "2012-10-26",
                description = "A systems administrator job",
                event = e1)

        j3 = Job(name = "Project Manager",
                start_date = "2012-1-2",
                end_date = "2012-2-2",
                description = "A management job",
                event = e1)

        j1.save()
        j2.save()
        j3.save()

        #test typical cases
        self.assertIsNotNone(get_job_by_id(j1.id))
        self.assertIsNotNone(get_job_by_id(j2.id))
        self.assertIsNotNone(get_job_by_id(j3.id))

        self.assertEqual(get_job_by_id(j1.id), j1)
        self.assertEqual(get_job_by_id(j2.id), j2)
        self.assertEqual(get_job_by_id(j3.id), j3)

        #test non-existant cases
        self.assertIsNone(get_job_by_id(100))
        self.assertIsNone(get_job_by_id(200))
        self.assertIsNone(get_job_by_id(300))
        self.assertIsNone(get_job_by_id(400))

        self.assertNotEqual(get_job_by_id(100), j1)
        self.assertNotEqual(get_job_by_id(100), j2)
        self.assertNotEqual(get_job_by_id(100), j3)
        self.assertNotEqual(get_job_by_id(200), j1)
        self.assertNotEqual(get_job_by_id(200), j2)
        self.assertNotEqual(get_job_by_id(200), j3)
        self.assertNotEqual(get_job_by_id(300), j1)
        self.assertNotEqual(get_job_by_id(300), j2)
        self.assertNotEqual(get_job_by_id(300), j3)

    def test_get_jobs_ordered_by_title(self):

        e1 = Event(name = "Software Conference",
                start_date = "2012-10-22",
                end_date = "2012-10-25")

        e1.save()

        j1 = Job(name = "Software Developer",
                start_date = "2012-10-22",
                end_date = "2012-10-23",
                description = "A software job",
                event = e1)

        j2 = Job(name = "Systems Administrator",
                start_date = "2012-9-1",
                end_date = "2012-10-26",
                description = "A systems administrator job",
                event = e1)

        j3 = Job(name = "Project Manager",
                start_date = "2012-1-2",
                end_date = "2012-2-2",
                description = "A management job",
                event = e1)

        j1.save()
        j2.save()
        j3.save()       
                    
        #test typical case
        job_list = get_jobs_ordered_by_title()
        self.assertIsNotNone(job_list)
        self.assertNotEqual(job_list, False)
        self.assertEqual(len(job_list), 3)
        self.assertIn(j1, job_list)
        self.assertIn(j2, job_list)
        self.assertIn(j3, job_list)

        #test order
        self.assertEqual(job_list[0].name, j3.name)
        self.assertEqual(job_list[1].name, j1.name)
        self.assertEqual(job_list[2].name, j2.name)
