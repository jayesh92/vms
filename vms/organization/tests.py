from django.test import TestCase
from organization.models import Organization
from organization.services import *

class OrganizationMethodTests(TestCase):

    def test_get_organization_by_id(self):

        o1 = Organization(organization_name = "Google")
        o2 = Organization(organization_name = "Yahoo")
        o3 = Organization(organization_name = "Ubisoft")

        o1.save()
        o2.save()
        o3.save()

        #test typical cases
        self.assertIsNotNone(get_organization_by_id(o1.id))
        self.assertIsNotNone(get_organization_by_id(o2.id))
        self.assertIsNotNone(get_organization_by_id(o3.id))

        self.assertEqual(get_organization_by_id(o1.id), o1)
        self.assertEqual(get_organization_by_id(o2.id), o2)
        self.assertEqual(get_organization_by_id(o3.id), o3)

        self.assertIsNone(get_organization_by_id(100))
        self.assertIsNone(get_organization_by_id(200))
        self.assertIsNone(get_organization_by_id(300))

        self.assertNotEqual(get_organization_by_id(100), o1)
        self.assertNotEqual(get_organization_by_id(200), o1)
        self.assertNotEqual(get_organization_by_id(300), o1)

        self.assertNotEqual(get_organization_by_id(100), o2)
        self.assertNotEqual(get_organization_by_id(200), o2)
        self.assertNotEqual(get_organization_by_id(300), o2)

        self.assertNotEqual(get_organization_by_id(100), o3)
        self.assertNotEqual(get_organization_by_id(200), o3)
        self.assertNotEqual(get_organization_by_id(300), o3)

    def test_get_organization_by_name(self):

        o1 = Organization(organization_name = "Google")
        o2 = Organization(organization_name = "Yahoo")
        o3 = Organization(organization_name = "Ubisoft")
        o4 = Organization(organization_name = "IBM")
        o5 = Organization(organization_name = "Cisco")

        o1.save()
        o2.save()
        o3.save()
        o4.save()
        o5.save()

        #test typical cases
        organization_list = get_organizations_by_name()
        self.assertIsNotNone(organization_list)
        self.assertIn(o1, organization_list)
        self.assertIn(o2, organization_list)
        self.assertIn(o3, organization_list)
        self.assertIn(o4, organization_list)
        self.assertIn(o5, organization_list)
        self.assertEqual(len(organization_list), 5)

        #test order
        self.assertEqual(organization_list[0], o5)
        self.assertEqual(organization_list[1], o1)
        self.assertEqual(organization_list[2], o4)
        self.assertEqual(organization_list[3], o3)
        self.assertEqual(organization_list[4], o2)
