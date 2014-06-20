from django.contrib.auth.models import User
from django.test import TestCase
from job.models import Job, VolunteerShift
from job.services import *
from volunteer.models import Volunteer
from volunteer.services import *

class JobMethodTests(TestCase):

    def test_get_job_by_id(self):

        j1 = Job(job_title = "Software Developer",
                start_date = "2012-10-22",
                end_date = "2012-10-23",
                description = "A software job")

        j2 = Job(job_title = "Systems Administrator",
                start_date = "2012-9-1",
                end_date = "2012-10-26",
                description = "A systems administrator job")

        j3 = Job(job_title = "Project Manager",
                start_date = "2012-1-2",
                end_date = "2012-2-2",
                description = "A management job")

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

    def test_get_jobs_by_title(self):

        j1 = Job(job_title = "Software Developer",
                start_date = "2012-10-22",
                end_date = "2012-10-23",
                description = "A software job")

        j2 = Job(job_title = "Systems Administrator",
                start_date = "2012-9-1",
                end_date = "2012-10-26",
                description = "A systems administrator job")

        j3 = Job(job_title = "Project Manager",
                start_date = "2012-1-2",
                end_date = "2012-2-2",
                description = "A management job")

        j1.save()
        j2.save()
        j3.save()       
                    
        #test typical case
        job_list = get_jobs_by_title()
        self.assertIsNotNone(job_list)
        self.assertNotEqual(job_list, False)
        self.assertEqual(len(job_list), 3)
        self.assertIn(j1, job_list)
        self.assertIn(j2, job_list)
        self.assertIn(j3, job_list)

        #test order
        self.assertEqual(job_list[0].job_title, j3.job_title)
        self.assertEqual(job_list[1].job_title, j1.job_title)
        self.assertEqual(job_list[2].job_title, j2.job_title)

    def test_is_signed_up(self):

        u1 = User.objects.create_user('Yoshi')     

        v1 = Volunteer(first_name = "Yoshi",
                        last_name = "Turtle",
                        address = "Mario Land",
                        city = "Nintendo Land",
                        state = "Nintendo State",
                        country = "Nintendo Nation",
                        phone_number = "2374983247",
                        company = "Turtle Corporation",
                        email = "yoshi@nintendo.com",
                        user = u1)

        v1.save()

        j1 = Job(job_title = "Software Developer",
                start_date = "2012-10-22",
                end_date = "2012-10-23",
                description = "A software job")

        j2 = Job(job_title = "Systems Administrator",
                start_date = "2012-9-1",
                end_date = "2012-10-26",
                description = "A systems administrator job")
        
        j1.save()
        j2.save()

        s1 = Shift(date = "2012-10-23",
                    location = "Google Drive",
                    start_time = "9:00",
                    end_time = "3:00",
                    max_volunteers = 1,
                    job = j1)

        s2 = Shift(date = "2012-10-23",
                    location = "Infinite Loop",
                    start_time = "10:00",
                    end_time = "4:00",
                    max_volunteers = 2,
                    job = j1)

        s3 = Shift(date = "2012-10-23",
                    location = "Loopy Loop Road",
                    start_time = "12:00",
                    end_time = "6:00",
                    max_volunteers = 4,
                    job = j2)

        s1.save()
        s2.save()
        s3.save()
    
        #test cases where not signed up
        self.assertFalse(is_signed_up(v1.id, s1.id))
        self.assertFalse(is_signed_up(v1.id, s2.id))
        self.assertFalse(is_signed_up(v1.id, s3.id))

        #test cases where signed up
        register(v1.id, s1.id)
        register(v1.id, s2.id)
        register(v1.id, s3.id)

        self.assertTrue(is_signed_up(v1.id, s1.id))
        self.assertTrue(is_signed_up(v1.id, s2.id))
        self.assertTrue(is_signed_up(v1.id, s3.id))

        #test case: can multiple volunteers sign up for the same job?

    def test_register(self):

        u1 = User.objects.create_user('Yoshi')     

        v1 = Volunteer(first_name = "Yoshi",
                        last_name = "Turtle",
                        address = "Mario Land",
                        city = "Nintendo Land",
                        state = "Nintendo State",
                        country = "Nintendo Nation",
                        phone_number = "2374983247",
                        company = "Turtle Corporation",
                        email = "yoshi@nintendo.com",
                        user = u1)

        v1.save()

        j1 = Job(job_title = "Software Developer",
                start_date = "2012-10-22",
                end_date = "2012-10-23",
                description = "A software job")

        j2 = Job(job_title = "Systems Administrator",
                start_date = "2012-9-1",
                end_date = "2012-10-26",
                description = "A systems administrator job")
        
        j1.save()
        j2.save()

        s1 = Shift(date = "2012-10-23",
                    location = "Google Drive",
                    start_time = "9:00",
                    end_time = "3:00",
                    max_volunteers = 1,
                    job = j1)

        s2 = Shift(date = "2012-10-23",
                    location = "Infinite Loop",
                    start_time = "10:00",
                    end_time = "4:00",
                    max_volunteers = 2,
                    job = j1)

        s3 = Shift(date = "2012-10-23",
                    location = "Loopy Loop Road",
                    start_time = "12:00",
                    end_time = "6:00",
                    max_volunteers = 4,
                    job = j2)

        s1.save()
        s2.save()
        s3.save()
    
        #test typical cases
        self.assertTrue(register(v1.id, s1.id))
        self.assertIsNotNone(VolunteerShift.objects.get(volunteer_id=v1.id, shift_id=s1.id))

        self.assertTrue(register(v1.id, s2.id))
        self.assertIsNotNone(VolunteerShift.objects.get(volunteer_id=v1.id, shift_id=s2.id))

        self.assertTrue(register(v1.id, s3.id))
        self.assertIsNotNone(VolunteerShift.objects.get(volunteer_id=v1.id, shift_id=s3.id))

        #test cases where volunteer tries to sign up for a shift they are already signed up for
        self.assertFalse(register(v1.id, s1.id))
        self.assertFalse(register(v1.id, s2.id))
        self.assertFalse(register(v1.id, s3.id))

        #test case: can multiple volunteers sign up for the same job?
