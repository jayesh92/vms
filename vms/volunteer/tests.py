import datetime
from django.test import TestCase
from volunteer.models import Volunteer
from volunteer.services import *

class VolunteerMethodTests(TestCase):

    def test_get_volunteer_by_id(self):

        v1 = Volunteer(first_name = "John",
                        last_name = "Doe",
                        address = "7 Alpine Street",
                        city = "Maplegrove",
                        state = "Wyoming",
                        country = "USA",
                        phone_number = "23454545",
                        company = "Google",
                        email = "john@test.com")

        v2 = Volunteer(first_name = "James",
                        last_name = "Doe",
                        address = "7 Oak Street",
                        city = "Elmgrove",
                        state = "California",
                        country = "USA",
                        phone_number = "23454545",
                        company = "IBM",
                        email = "james@test.com")

        v3 = Volunteer(id = 999,
                        first_name = "George",
                        last_name = "Doe",
                        address = "7 Elm Street",
                        city = "Oakgrove",
                        state = "California",
                        country = "USA",
                        phone_number = "23454545",
                        company = "IBM",
                        email = "george@test.com")

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
    
        #test nonexistant cases 
        self.assertIsNone(get_volunteer_by_id(100))
        self.assertIsNone(get_volunteer_by_id(200))
        self.assertIsNone(get_volunteer_by_id(300))
        self.assertIsNone(get_volunteer_by_id(400))

        self.assertNotEqual(get_volunteer_by_id(100), v1)
        self.assertNotEqual(get_volunteer_by_id(200), v1)
        self.assertNotEqual(get_volunteer_by_id(300), v2)
        self.assertNotEqual(get_volunteer_by_id(400), v2)

    def test_get_volunteer_resume_file(self):
 
        v1 = Volunteer(first_name = "John",
                        last_name = "Doe",
                        address = "7 Alpine Street",
                        city = "Maplegrove",
                        state = "Wyoming",
                        country = "USA",
                        phone_number = "23454545",
                        company = "Google",
                        email = "john@test.com",
                        resume_file = "MyResume.pdf")

        v1.save()

        #test typical cases
        self.assertIsNotNone(get_volunteer_resume_file(v1.id))
        self.assertEquals(get_volunteer_resume_file(v1.id), v1.resume_file)

        #test nonexistant cases
        self.assertNotEquals(get_volunteer_resume_file(v1.id), "DifferentResume.pdf")
        self.assertNotEquals(get_volunteer_resume_file(v1.id), "AnotherResume.pdf")

    def test_get_volunteer_resume_file_url(self):

        v1 = Volunteer(first_name = "John",
                        last_name = "Doe",
                        address = "7 Alpine Street",
                        city = "Maplegrove",
                        state = "Wyoming",
                        country = "USA",
                        phone_number = "23454545",
                        company = "Google",
                        email = "john@test.com",
                        resume_file = "MyResume.pdf")

        v1.save()

        #test typicl cases
        self.assertIsNotNone(get_volunteer_resume_file_url(v1.id))
        self.assertEquals(get_volunteer_resume_file_url(v1.id), v1.resume_file.url)

        #test nonexistant cases
        self.assertNotEquals(get_volunteer_resume_file_url(v1.id), "resumes/DifferentResume.pdf")
        self.assertNotEquals(get_volunteer_resume_file_url(v1.id), "resumes/AnotherResume.pdf")

    def test_get_volunteers_by_first_name(self):

        v1 = Volunteer(first_name = "Yoshi",
                        last_name = "Doe",
                        address = "7 Oak Street",
                        city = "Elmgrove",
                        state = "California",
                        country = "USA",
                        phone_number = "23454545",
                        company = "IBM",
                        email = "yoshi@test.com")

        v2 = Volunteer(first_name = "Ashley",
                        last_name = "Doe",
                        address = "7 Alpine Street",
                        city = "Maplegrove",
                        state = "Wyoming",
                        country = "USA",
                        phone_number = "23454545",
                        company = "Google",
                        email = "ashley@test.com")

        v3 = Volunteer(id = 999,
                        first_name = "Zelda",
                        last_name = "Doe",
                        address = "7 Elm Street",
                        city = "Oakgrove",
                        state = "California",
                        country = "USA",
                        phone_number = "23454545",
                        company = "IBM",
                        email = "zelda@test.com")

        v1.save()
        v2.save()
        v3.save()

        #test typical cases
        self.assertIsNotNone(get_volunteers_by_first_name())
        self.assertIn(v1, get_volunteers_by_first_name())
        self.assertIn(v2, get_volunteers_by_first_name())
        self.assertIn(v3, get_volunteers_by_first_name())
        self.assertEquals(len(get_volunteers_by_first_name()), 3)

        #test if in correct order
        self.assertEquals(get_volunteers_by_first_name()[0], v2)
        self.assertEquals(get_volunteers_by_first_name()[1], v1)
        self.assertEquals(get_volunteers_by_first_name()[2], v3)

    def test_search_volunteers(self):
 
        v1 = Volunteer(first_name = "Yoshi",
                        last_name = "Doe",
                        address = "7 Oak Street",
                        city = "Elmgrove",
                        state = "California",
                        country = "USA",
                        phone_number = "23454545",
                        company = "IBM",
                        email = "yoshi@test.com")

        v2 = Volunteer(first_name = "Ashley",
                        last_name = "Doe",
                        address = "7 Alpine Street",
                        city = "Maplegrove",
                        state = "Wyoming",
                        country = "USA",
                        phone_number = "23454545",
                        company = "Google",
                        email = "ashley@test.com")

        v3 = Volunteer(id = 999,
                        first_name = "Zelda",
                        last_name = "Doe",
                        address = "7 Elm Street",
                        city = "Oakgrove",
                        state = "California",
                        country = "USA",
                        phone_number = "23454545",
                        company = "IBM",
                        email = "zelda@test.com")               

        v1.save()
        v2.save()
        v3.save()

        #if no search parameters are given, it returns all volunteers 
        search_list = search_volunteers("", "", "", "", "", "")
        self.assertNotEquals(search_list, False)
        self.assertEquals(len(search_list), 3)
        self.assertIn(v1, search_list)
        self.assertIn(v2, search_list)
        self.assertIn(v3, search_list)

        search_list = search_volunteers(None, None, None, None, None, None)
        self.assertNotEquals(search_list, False)
        self.assertEquals(len(search_list), 3)
        self.assertIn(v1, search_list)
        self.assertIn(v2, search_list)
        self.assertIn(v3, search_list)

        #test exact search
        search_list = search_volunteers("Yoshi", "Doe", "Elmgrove", "California", "USA", "IBM")
        self.assertNotEquals(search_list, False)
        self.assertEquals(len(search_list), 1)
        self.assertIn(v1, search_list)
        self.assertNotIn(v2, search_list)
        self.assertNotIn(v3, search_list)

        #test partial search
        search_list = search_volunteers("Yoshi", None, None, None, None, None)
        self.assertNotEquals(search_list, False)
        self.assertEquals(len(search_list), 1)
        self.assertIn(v1, search_list)
        self.assertNotIn(v2, search_list)
        self.assertNotIn(v3, search_list)

        search_list = search_volunteers(None, "Doe", None, None, None, None)
        self.assertNotEquals(search_list, False)
        self.assertEquals(len(search_list), 3)
        self.assertIn(v1, search_list)
        self.assertIn(v2, search_list)
        self.assertIn(v3, search_list)

        #test no search matches
        search_list = search_volunteers("Billy", "Doe", "Montreal", "Quebec", "Canada", "Ubisoft")
        self.assertEquals(len(search_list), 0)
        self.assertNotIn(v1, search_list)
        self.assertNotIn(v2, search_list)
        self.assertNotIn(v3, search_list)

