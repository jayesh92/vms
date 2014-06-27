import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from volunteer.models import Volunteer
from volunteer.services import *

class VolunteerMethodTests(TestCase):

    def test_get_volunteer_by_id(self):

        u1 = User.objects.create_user('John')
        u2 = User.objects.create_user('James')
        u3 = User.objects.create_user('George')

        v1 = Volunteer(first_name = "John",
                        last_name = "Doe",
                        address = "7 Alpine Street",
                        city = "Maplegrove",
                        state = "Wyoming",
                        country = "USA",
                        phone_number = "23454545",
                        email = "john@test.com",
                        user = u1)

        v2 = Volunteer(first_name = "James",
                        last_name = "Doe",
                        address = "7 Oak Street",
                        city = "Elmgrove",
                        state = "California",
                        country = "USA",
                        phone_number = "23454545",
                        email = "james@test.com",
                        user = u2)

        v3 = Volunteer(id = 999,
                        first_name = "George",
                        last_name = "Doe",
                        address = "7 Elm Street",
                        city = "Oakgrove",
                        state = "California",
                        country = "USA",
                        phone_number = "23454545",
                        email = "george@test.com",
                        user = u3)

        v1.save()
        v2.save()
        v3.save()

        #test typical cases
        self.assertIsNotNone(get_volunteer_by_id(v1.id))
        self.assertIsNotNone(get_volunteer_by_id(v2.id))
        self.assertIsNotNone(get_volunteer_by_id(v3.id))

        self.assertEqual(get_volunteer_by_id(v1.id), v1)
        self.assertEqual(get_volunteer_by_id(v2.id), v2)
        self.assertEqual(get_volunteer_by_id(v3.id), v3)

        #why doesn't testing for equality work?
        #self.assertIs(get_volunteer_by_id(v1.id), v1)
        #self.assertIs(get_volunteer_by_id(v2.id), v2)
        #self.assertIs(get_volunteer_by_id(v3.id), v3)
    
        #test non-existant cases 
        self.assertIsNone(get_volunteer_by_id(100))
        self.assertIsNone(get_volunteer_by_id(200))
        self.assertIsNone(get_volunteer_by_id(300))
        self.assertIsNone(get_volunteer_by_id(400))

        self.assertNotEqual(get_volunteer_by_id(100), v1)
        self.assertNotEqual(get_volunteer_by_id(200), v1)
        self.assertNotEqual(get_volunteer_by_id(300), v2)
        self.assertNotEqual(get_volunteer_by_id(400), v2)

    def test_has_resume_file(self):
 
        u1 = User.objects.create_user('John')
        u2 = User.objects.create_user('James')
        u3 = User.objects.create_user('Jane')

        v1 = Volunteer(first_name = "John",
                        last_name = "Doe",
                        address = "7 Alpine Street",
                        city = "Maplegrove",
                        state = "Wyoming",
                        country = "USA",
                        phone_number = "23454545",
                        email = "john@test.com",
                        resume_file = "MyResume.pdf",
                        user = u1)

        v2 = Volunteer(first_name = "James",
                        last_name = "Doe",
                        address = "7 Alpine Street",
                        city = "Maplegrove",
                        state = "Wyoming",
                        country = "USA",
                        phone_number = "23454545",
                        email = "james@test.com",
                        user = u2)

        v3 = Volunteer(first_name = "Jane",
                        last_name = "Doe",
                        address = "7 Alpine Street",
                        city = "Maplegrove",
                        state = "Wyoming",
                        country = "USA",
                        phone_number = "23454545",
                        email = "jane@test.com",
                        resume_file = "",
                        user = u3)

        v1.save()
        v2.save()
        v3.save()

        #test typical cases
        self.assertTrue(has_resume_file(v1.id))

        #test non-existant cases
        self.assertFalse(has_resume_file(v2.id))
        self.assertFalse(has_resume_file(v3.id))

    def test_get_volunteer_resume_file_url(self):

        u1 = User.objects.create_user('John')

        v1 = Volunteer(first_name = "John",
                        last_name = "Doe",
                        address = "7 Alpine Street",
                        city = "Maplegrove",
                        state = "Wyoming",
                        country = "USA",
                        phone_number = "23454545",
                        email = "john@test.com",
                        resume_file = "MyResume.pdf",
                        user = u1)

        v1.save()

        #test typicl cases
        self.assertIsNotNone(get_volunteer_resume_file_url(v1.id))
        self.assertEqual(get_volunteer_resume_file_url(v1.id), v1.resume_file.url)

        #test non-existant cases
        self.assertNotEqual(get_volunteer_resume_file_url(v1.id), "resumes/DifferentResume.pdf")
        self.assertNotEqual(get_volunteer_resume_file_url(v1.id), "resumes/AnotherResume.pdf")

    def test_get_volunteers_by_first_name(self):

        u1 = User.objects.create_user('Yoshi')
        u2 = User.objects.create_user('Ashley')
        u3 = User.objects.create_user('Zelda')

        v1 = Volunteer(first_name = "Yoshi",
                        last_name = "Doe",
                        address = "7 Oak Street",
                        city = "Elmgrove",
                        state = "California",
                        country = "USA",
                        phone_number = "23454545",
                        email = "yoshi@test.com",
                        user = u1)

        v2 = Volunteer(first_name = "Ashley",
                        last_name = "Doe",
                        address = "7 Alpine Street",
                        city = "Maplegrove",
                        state = "Wyoming",
                        country = "USA",
                        phone_number = "23454545",
                        email = "ashley@test.com",
                        user = u2)

        v3 = Volunteer(id = 999,
                        first_name = "Zelda",
                        last_name = "Doe",
                        address = "7 Elm Street",
                        city = "Oakgrove",
                        state = "California",
                        country = "USA",
                        phone_number = "23454545",
                        email = "zelda@test.com",
                        user = u3)

        v1.save()
        v2.save()
        v3.save()

        #test typical cases
        volunteer_list = get_volunteers_by_first_name()
        self.assertIsNotNone(volunteer_list)
        self.assertIn(v1, volunteer_list)
        self.assertIn(v2, volunteer_list)
        self.assertIn(v3, volunteer_list)
        self.assertEqual(len(volunteer_list), 3)

        #test if in correct order
        self.assertEqual(volunteer_list[0], v2)
        self.assertEqual(volunteer_list[1], v1)
        self.assertEqual(volunteer_list[2], v3)

    def test_search_volunteers(self):
 
        u1 = User.objects.create_user('Yoshi')
        u2 = User.objects.create_user('Ashley')
        u3 = User.objects.create_user('Zelda')

        v1 = Volunteer(first_name = "Yoshi",
                        last_name = "Doe",
                        address = "7 Oak Street",
                        city = "Elmgrove",
                        state = "California",
                        country = "USA",
                        phone_number = "23454545",
                        email = "yoshi@test.com",
                        user = u1)

        v2 = Volunteer(first_name = "Ashley",
                        last_name = "Doe",
                        address = "7 Alpine Street",
                        city = "Maplegrove",
                        state = "Wyoming",
                        country = "USA",
                        phone_number = "23454545",
                        email = "ashley@test.com",
                        user = u2)

        v3 = Volunteer(id = 999,
                        first_name = "Zelda",
                        last_name = "Doe",
                        address = "7 Elm Street",
                        city = "Oakgrove",
                        state = "California",
                        country = "USA",
                        phone_number = "23454545",
                        email = "zelda@test.com",
                        user = u3)               

        v1.save()
        v2.save()
        v3.save()

        #if no search parameters are given, it returns all volunteers 
        search_list = search_volunteers("", "", "", "", "")
        self.assertNotEqual(search_list, False)
        self.assertEqual(len(search_list), 3)
        self.assertIn(v1, search_list)
        self.assertIn(v2, search_list)
        self.assertIn(v3, search_list)

        search_list = search_volunteers(None, None, None, None, None)
        self.assertNotEqual(search_list, False)
        self.assertEqual(len(search_list), 3)
        self.assertIn(v1, search_list)
        self.assertIn(v2, search_list)
        self.assertIn(v3, search_list)

        #test exact search
        search_list = search_volunteers("Yoshi", "Doe", "Elmgrove", "California", "USA")
        self.assertNotEqual(search_list, False)
        self.assertEqual(len(search_list), 1)
        self.assertIn(v1, search_list)
        self.assertNotIn(v2, search_list)
        self.assertNotIn(v3, search_list)

        #test partial search
        search_list = search_volunteers("Yoshi", None, None, None, None)
        self.assertNotEqual(search_list, False)
        self.assertEqual(len(search_list), 1)
        self.assertIn(v1, search_list)
        self.assertNotIn(v2, search_list)
        self.assertNotIn(v3, search_list)

        search_list = search_volunteers(None, "Doe", None, None, None)
        self.assertNotEqual(search_list, False)
        self.assertEqual(len(search_list), 3)
        self.assertIn(v1, search_list)
        self.assertIn(v2, search_list)
        self.assertIn(v3, search_list)

        #test no search matches
        search_list = search_volunteers("Billy", "Doe", "Montreal", "Quebec", "Canada")
        self.assertEqual(len(search_list), 0)
        self.assertNotIn(v1, search_list)
        self.assertNotIn(v2, search_list)
        self.assertNotIn(v3, search_list)

