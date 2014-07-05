import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from job.models import Job, VolunteerShift
from job.services import *
from volunteer.models import Volunteer
from volunteer.services import *

class JobMethodTests(TestCase):

    def test_calculate_working_duration(self):

        start_time = datetime.time(hour=1, minute=0) 
        end_time = datetime.time(hour=2, minute=0) 
        delta_time_hours = 1
        self.assertEqual(calculate_working_duration(start_time, end_time), delta_time_hours)

        start_time = datetime.time(hour=1, minute=45) 
        end_time = datetime.time(hour=2, minute=0) 
        delta_time_hours = 0.25
        self.assertEqual(calculate_working_duration(start_time, end_time), delta_time_hours)

        start_time = datetime.time(hour=1, minute=0) 
        end_time = datetime.time(hour=2, minute=30) 
        delta_time_hours = 1.5
        self.assertEqual(calculate_working_duration(start_time, end_time), delta_time_hours)

        start_time = datetime.time(hour=1, minute=0) 
        end_time = datetime.time(hour=1, minute=45) 
        delta_time_hours = 0.75
        self.assertEqual(calculate_working_duration(start_time, end_time), delta_time_hours)

        start_time = datetime.time(hour=1, minute=0) 
        end_time = datetime.time(hour=13, minute=0) 
        delta_time_hours = 12
        self.assertEqual(calculate_working_duration(start_time, end_time), delta_time_hours)

        start_time = datetime.time(hour=1, minute=0) 
        end_time = datetime.time(hour=5, minute=45) 
        delta_time_hours = 4.75 
        self.assertEqual(calculate_working_duration(start_time, end_time), delta_time_hours)

        start_time = datetime.time(hour=1, minute=0) 
        end_time = datetime.time(hour=1, minute=0) 
        delta_time_hours = 0 
        self.assertEqual(calculate_working_duration(start_time, end_time), delta_time_hours)

        start_time = datetime.time(hour=1, minute=0) 
        end_time = datetime.time(hour=23, minute=0) 
        delta_time_hours = 22 
        self.assertEqual(calculate_working_duration(start_time, end_time), delta_time_hours)

    def test_cancel_shift_registration(self):

        u1 = User.objects.create_user('Yoshi')     
        u2 = User.objects.create_user('John')     

        v1 = Volunteer(first_name = "Yoshi",
                        last_name = "Turtle",
                        address = "Mario Land",
                        city = "Nintendo Land",
                        state = "Nintendo State",
                        country = "Nintendo Nation",
                        phone_number = "2374983247",
                        email = "yoshi@nintendo.com",
                        user = u1)

        v2 = Volunteer(first_name = "John",
                        last_name = "Doe",
                        address = "7 Alpine Street",
                        city = "Maplegrove",
                        state = "Wyoming",
                        country = "USA",
                        phone_number = "23454545",
                        email = "john@test.com",
                        user = u2)

        v1.save()
        v2.save()

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
                    slots_remaining = 2,
                    job = j1)

        s2 = Shift(date = "2012-10-23",
                    location = "Infinite Loop",
                    start_time = "10:00",
                    end_time = "4:00",
                    max_volunteers = 2,
                    slots_remaining = 2,
                    job = j1)

        s3 = Shift(date = "2012-10-23",
                    location = "Loopy Loop Road",
                    start_time = "12:00",
                    end_time = "6:00",
                    max_volunteers = 4,
                    slots_remaining = 4,
                    job = j2)

        s1.save()
        s2.save()
        s3.save()

        #test cases when try to cancel when they aren't signed up for a shift
        self.assertFalse(cancel_shift_registration(v1.id, s1.id))
        self.assertFalse(cancel_shift_registration(v1.id, s2.id))
        self.assertFalse(cancel_shift_registration(v1.id, s3.id))
        self.assertFalse(cancel_shift_registration(v2.id, s1.id))
        self.assertFalse(cancel_shift_registration(v2.id, s2.id))
        self.assertFalse(cancel_shift_registration(v2.id, s3.id))

        #register volunteers to shifts
        self.assertTrue(register(v1.id, s1.id))
        self.assertTrue(register(v1.id, s2.id))
        self.assertTrue(register(v1.id, s3.id))
        self.assertTrue(register(v2.id, s1.id))
        self.assertTrue(register(v2.id, s2.id))
        self.assertTrue(register(v2.id, s3.id))

        #test typical cases
        self.assertTrue(cancel_shift_registration(v1.id, s1.id))
        self.assertTrue(cancel_shift_registration(v1.id, s2.id))
        self.assertTrue(cancel_shift_registration(v1.id, s3.id))
        self.assertTrue(cancel_shift_registration(v2.id, s1.id))
        self.assertTrue(cancel_shift_registration(v2.id, s2.id))
        self.assertTrue(cancel_shift_registration(v2.id, s3.id))

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

    def test_get_shift_by_id(self):

        j1 = Job(job_title = "Software Developer",
                start_date = "2012-10-22",
                end_date = "2012-10-23",
                description = "A software job")
        
        j1.save()

        s1 = Shift(date = "2012-10-23",
                    location = "Google Drive",
                    start_time = "9:00",
                    end_time = "3:00",
                    max_volunteers = 1,
                    slots_remaining = 1,
                    job = j1)

        s2 = Shift(date = "2012-10-23",
                    location = "Infinite Loop",
                    start_time = "10:00",
                    end_time = "4:00",
                    max_volunteers = 2,
                    slots_remaining = 2,
                    job = j1)

        s3 = Shift(date = "2012-10-23",
                    location = "Loopy Loop Road",
                    start_time = "12:00",
                    end_time = "6:00",
                    max_volunteers = 4,
                    slots_remaining = 4,
                    job = j1)

        s1.save()
        s2.save()
        s3.save()

        #test typical cases
        self.assertIsNotNone(get_shift_by_id(s1.id))
        self.assertIsNotNone(get_shift_by_id(s2.id))
        self.assertIsNotNone(get_shift_by_id(s3.id))

        self.assertEqual(get_shift_by_id(s1.id), s1)
        self.assertEqual(get_shift_by_id(s2.id), s2)
        self.assertEqual(get_shift_by_id(s3.id), s3)

        #test non-existant cases
        self.assertIsNone(get_shift_by_id(100))
        self.assertIsNone(get_shift_by_id(200))
        self.assertIsNone(get_shift_by_id(300))
        self.assertIsNone(get_shift_by_id(400))

        self.assertNotEqual(get_shift_by_id(100), s1)
        self.assertNotEqual(get_shift_by_id(100), s2)
        self.assertNotEqual(get_shift_by_id(100), s3)
        self.assertNotEqual(get_shift_by_id(200), s1)
        self.assertNotEqual(get_shift_by_id(200), s2)
        self.assertNotEqual(get_shift_by_id(200), s3)
        self.assertNotEqual(get_shift_by_id(300), s1)
        self.assertNotEqual(get_shift_by_id(300), s2)
        self.assertNotEqual(get_shift_by_id(300), s3)

    def get_shifts_by_date(self):

        j1 = Job(job_title = "Software Developer",
                start_date = "2012-10-22",
                end_date = "2012-10-23",
                description = "A software job")
        
        j1.save()

        s1 = Shift(date = "2012-1-10",
                    location = "Google Drive",
                    start_time = "9:00",
                    end_time = "3:00",
                    max_volunteers = 1,
                    slots_remaining = 1,
                    job = j1)

        s2 = Shift(date = "2012-6-25",
                    location = "Infinite Loop",
                    start_time = "10:00",
                    end_time = "4:00",
                    max_volunteers = 2,
                    slots_remaining = 2,
                    job = j1)

        s3 = Shift(date = "2012-12-9",
                    location = "Loopy Loop Road",
                    start_time = "12:00",
                    end_time = "6:00",
                    max_volunteers = 4,
                    slots_remaining = 4,
                    job = j1)

        s1.save()
        s2.save()
        s3.save()

        #test typical case
        shift_list = get_shifts_by_date(j1.id)
        self.assertIsNotNone(shift_list)
        self.assertNotEqual(shift_list, False)
        self.assertEqual(len(shift_list), 3)
        self.assertIn(s1, shift_list)
        self.assertIn(s2, shift_list)
        self.assertIn(s3, shift_list)

        #test order
        self.assertEqual(shift_list[0].date, s1.date)
        self.assertEqual(shift_list[1].date, s2.date)
        self.assertEqual(shift_list[2].date, s3.date)

    def test_get_shifts_signed_up_for(self):

        u1 = User.objects.create_user('Yoshi')     

        v1 = Volunteer(first_name = "Yoshi",
                        last_name = "Turtle",
                        address = "Mario Land",
                        city = "Nintendo Land",
                        state = "Nintendo State",
                        country = "Nintendo Nation",
                        phone_number = "2374983247",
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
                    slots_remaining = 1,
                    job = j1)

        s2 = Shift(date = "2012-10-23",
                    location = "Infinite Loop",
                    start_time = "10:00",
                    end_time = "4:00",
                    max_volunteers = 2,
                    slots_remaining = 2,
                    job = j1)

        s3 = Shift(date = "2012-10-23",
                    location = "Loopy Loop Road",
                    start_time = "12:00",
                    end_time = "6:00",
                    max_volunteers = 4,
                    slots_remaining = 4,
                    job = j2)

        s1.save()
        s2.save()
        s3.save()
    
        #sign up
        register(v1.id, s1.id)
        register(v1.id, s2.id)
        register(v1.id, s3.id)

        #test typical case
        shift_list = get_shifts_signed_up_for(v1.id)
        self.assertIsNotNone(shift_list)
        self.assertNotEqual(shift_list, False)
        self.assertEqual(len(shift_list), 3)
        self.assertIn(s1, shift_list)
        self.assertIn(s2, shift_list)
        self.assertIn(s3, shift_list)

    def test_get_volunteer_shift_by_id(self):
        
        u1 = User.objects.create_user('Yoshi')     
        u2 = User.objects.create_user('John')     

        v1 = Volunteer(first_name = "Yoshi",
                        last_name = "Turtle",
                        address = "Mario Land",
                        city = "Nintendo Land",
                        state = "Nintendo State",
                        country = "Nintendo Nation",
                        phone_number = "2374983247",
                        email = "yoshi@nintendo.com",
                        user = u1)

        v2 = Volunteer(first_name = "John",
                        last_name = "Doe",
                        address = "7 Alpine Street",
                        city = "Maplegrove",
                        state = "Wyoming",
                        country = "USA",
                        phone_number = "23454545",
                        email = "john@test.com",
                        user = u2)

        v1.save()
        v2.save()

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
                    slots_remaining = 2,
                    job = j1)

        s2 = Shift(date = "2012-10-23",
                    location = "Infinite Loop",
                    start_time = "10:00",
                    end_time = "4:00",
                    max_volunteers = 2,
                    slots_remaining = 2,
                    job = j1)

        s3 = Shift(date = "2012-10-23",
                    location = "Loopy Loop Road",
                    start_time = "12:00",
                    end_time = "6:00",
                    max_volunteers = 4,
                    slots_remaining = 4,
                    job = j2)

        s1.save()
        s2.save()
        s3.save()
    
        #test cases where signed up
        self.assertTrue(register(v1.id, s1.id))
        self.assertTrue(register(v1.id, s2.id))
        self.assertTrue(register(v1.id, s3.id))

        self.assertTrue(register(v2.id, s1.id))
        self.assertTrue(register(v2.id, s2.id))
        self.assertTrue(register(v2.id, s3.id))

        self.assertEqual(get_volunteer_shift_by_id(v1.id, s1.id), VolunteerShift.objects.get(volunteer_id=v1.id, shift_id=s1.id))
        self.assertEqual(get_volunteer_shift_by_id(v1.id, s2.id), VolunteerShift.objects.get(volunteer_id=v1.id, shift_id=s2.id))
        self.assertEqual(get_volunteer_shift_by_id(v1.id, s3.id), VolunteerShift.objects.get(volunteer_id=v1.id, shift_id=s3.id))

        self.assertEqual(get_volunteer_shift_by_id(v2.id, s1.id), VolunteerShift.objects.get(volunteer_id=v2.id, shift_id=s1.id))
        self.assertEqual(get_volunteer_shift_by_id(v2.id, s2.id), VolunteerShift.objects.get(volunteer_id=v2.id, shift_id=s2.id))
        self.assertEqual(get_volunteer_shift_by_id(v2.id, s3.id), VolunteerShift.objects.get(volunteer_id=v2.id, shift_id=s3.id))

    def test_decrement_slots_remaining(self):

        j1 = Job(job_title = "Software Developer",
                start_date = "2012-10-22",
                end_date = "2012-10-23",
                description = "A software job")

        j1.save()

        s1 = Shift(date = "2012-10-23",
                    location = "Google Drive",
                    start_time = "9:00",
                    end_time = "3:00",
                    max_volunteers = 1,
                    slots_remaining = 4,
                    job = j1)

        s1.save()

        self.assertEqual(s1.slots_remaining, 4)
        decrement_slots_remaining(s1)

        self.assertEqual(s1.slots_remaining, 3)
        decrement_slots_remaining(s1)

        self.assertEqual(s1.slots_remaining, 2)
        decrement_slots_remaining(s1)

        self.assertEqual(s1.slots_remaining, 1)
        decrement_slots_remaining(s1)

        self.assertEqual(s1.slots_remaining, 0)

    def test_has_slots_remaining(self):

        j1 = Job(job_title = "Software Developer",
                start_date = "2012-10-22",
                end_date = "2012-10-23",
                description = "A software job")
        
        j1.save()

        s1 = Shift(date = "2012-10-23",
                    location = "Google Drive",
                    start_time = "9:00",
                    end_time = "3:00",
                    max_volunteers = 1,
                    slots_remaining = 1,
                    job = j1)

        s2 = Shift(date = "2012-10-23",
                    location = "Infinite Loop",
                    start_time = "10:00",
                    end_time = "4:00",
                    max_volunteers = 2,
                    slots_remaining = 2,
                    job = j1)

        s3 = Shift(date = "2012-10-23",
                    location = "Loopy Loop Road",
                    start_time = "12:00",
                    end_time = "6:00",
                    max_volunteers = 4,
                    slots_remaining = 4,
                    job = j1)

        s1.save()
        s2.save()
        s3.save()

        self.assertTrue(has_slots_remaining(s1))
        self.assertTrue(has_slots_remaining(s2))
        self.assertTrue(has_slots_remaining(s3))

        decrement_slots_remaining(s1)
        self.assertFalse(has_slots_remaining(s1))

        decrement_slots_remaining(s2)
        self.assertTrue(has_slots_remaining(s2))
        decrement_slots_remaining(s2)
        self.assertFalse(has_slots_remaining(s2))

        decrement_slots_remaining(s3)
        self.assertTrue(has_slots_remaining(s3))
        decrement_slots_remaining(s3)
        self.assertTrue(has_slots_remaining(s3))
        decrement_slots_remaining(s3)
        self.assertTrue(has_slots_remaining(s3))
        decrement_slots_remaining(s3)
        self.assertFalse(has_slots_remaining(s3))

        self.assertEqual(s1.slots_remaining, 0)
        self.assertEqual(s2.slots_remaining, 0)
        self.assertEqual(s3.slots_remaining, 0)

    def test_increment_slots_remaining(self):

        j1 = Job(job_title = "Software Developer",
                start_date = "2012-10-22",
                end_date = "2012-10-23",
                description = "A software job")

        j1.save()

        s1 = Shift(date = "2012-10-23",
                    location = "Google Drive",
                    start_time = "9:00",
                    end_time = "3:00",
                    max_volunteers = 1,
                    slots_remaining = 0,
                    job = j1)

        s1.save()

        self.assertEqual(s1.slots_remaining, 0)
        increment_slots_remaining(s1)

        self.assertEqual(s1.slots_remaining, 1)
        increment_slots_remaining(s1)

        self.assertEqual(s1.slots_remaining, 2)
        increment_slots_remaining(s1)

        self.assertEqual(s1.slots_remaining, 3)
        increment_slots_remaining(s1)

        self.assertEqual(s1.slots_remaining, 4)

    def test_is_signed_up(self):

        u1 = User.objects.create_user('Yoshi')     
        u2 = User.objects.create_user('John')     

        v1 = Volunteer(first_name = "Yoshi",
                        last_name = "Turtle",
                        address = "Mario Land",
                        city = "Nintendo Land",
                        state = "Nintendo State",
                        country = "Nintendo Nation",
                        phone_number = "2374983247",
                        email = "yoshi@nintendo.com",
                        user = u1)

        v2 = Volunteer(first_name = "John",
                        last_name = "Doe",
                        address = "7 Alpine Street",
                        city = "Maplegrove",
                        state = "Wyoming",
                        country = "USA",
                        phone_number = "23454545",
                        email = "john@test.com",
                        user = u2)

        v1.save()
        v2.save()

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
                    slots_remaining = 1,
                    job = j1)

        s2 = Shift(date = "2012-10-23",
                    location = "Infinite Loop",
                    start_time = "10:00",
                    end_time = "4:00",
                    max_volunteers = 2,
                    slots_remaining = 2,
                    job = j1)

        s3 = Shift(date = "2012-10-23",
                    location = "Loopy Loop Road",
                    start_time = "12:00",
                    end_time = "6:00",
                    max_volunteers = 4,
                    slots_remaining = 4,
                    job = j2)

        s1.save()
        s2.save()
        s3.save()
    
        #test cases where not signed up yet
        self.assertFalse(is_signed_up(v1.id, s1.id))
        self.assertFalse(is_signed_up(v1.id, s2.id))
        self.assertFalse(is_signed_up(v1.id, s3.id))

        #test cases where signed up
        self.assertTrue(register(v1.id, s1.id))
        self.assertTrue(register(v1.id, s2.id))
        self.assertTrue(register(v1.id, s3.id))

        self.assertTrue(is_signed_up(v1.id, s1.id))
        self.assertTrue(is_signed_up(v1.id, s2.id))
        self.assertTrue(is_signed_up(v1.id, s3.id))

        #test case where more than one volunteer signs up for the same shift
        self.assertFalse(is_signed_up(v2.id, s1.id))
        self.assertFalse(is_signed_up(v2.id, s2.id))
        self.assertFalse(is_signed_up(v2.id, s3.id))

        self.assertFalse(register(v2.id, s1.id))
        self.assertTrue(register(v2.id, s2.id))
        self.assertTrue(register(v2.id, s3.id))

        self.assertFalse(is_signed_up(v2.id, s1.id))
        self.assertTrue(is_signed_up(v2.id, s2.id))
        self.assertTrue(is_signed_up(v2.id, s3.id))

    def test_register(self):

        u1 = User.objects.create_user('Yoshi')     
        u2 = User.objects.create_user('John')     

        v1 = Volunteer(first_name = "Yoshi",
                        last_name = "Turtle",
                        address = "Mario Land",
                        city = "Nintendo Land",
                        state = "Nintendo State",
                        country = "Nintendo Nation",
                        phone_number = "2374983247",
                        email = "yoshi@nintendo.com",
                        user = u1)

        v2 = Volunteer(first_name = "John",
                        last_name = "Doe",
                        address = "7 Alpine Street",
                        city = "Maplegrove",
                        state = "Wyoming",
                        country = "USA",
                        phone_number = "23454545",
                        email = "john@test.com",
                        user = u2)

        v1.save()
        v2.save()

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
                    slots_remaining = 1,
                    job = j1)

        s2 = Shift(date = "2012-10-23",
                    location = "Infinite Loop",
                    start_time = "10:00",
                    end_time = "4:00",
                    max_volunteers = 2,
                    slots_remaining = 2,
                    job = j1)

        s3 = Shift(date = "2012-10-23",
                    location = "Loopy Loop Road",
                    start_time = "12:00",
                    end_time = "6:00",
                    max_volunteers = 4,
                    slots_remaining = 4,
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

        #test case where more than one volunteer signs up for the same shift
        #v2 can't sign up for s1 because there are no slots remaining
        self.assertFalse(register(v2.id, s1.id))

        self.assertTrue(register(v2.id, s2.id))
        self.assertIsNotNone(VolunteerShift.objects.get(volunteer_id=v2.id, shift_id=s2.id))

        self.assertTrue(register(v2.id, s3.id))
        self.assertIsNotNone(VolunteerShift.objects.get(volunteer_id=v2.id, shift_id=s3.id))

        #test cases where a volunteer tries to sign up for a shift they are already signed up for
        self.assertFalse(register(v2.id, s2.id))
        self.assertFalse(register(v2.id, s3.id))
