from django.test import TestCase
from organization.models import Organization
from organization.services import *

class OrganizationMethodTests(TestCase):

    def test_get_organization_by_id(self):

        o1 = Organization(name = "Google")
        o2 = Organization(name = "Yahoo")
        o3 = Organization(name = "Ubisoft")

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

        o1 = Organization(name = "Google")
        o2 = Organization(name = "Yahoo")
        o3 = Organization(name = "Ubisoft")

        o1.save()
        o2.save()
        o3.save()

        #test typical cases
        self.assertIsNotNone(get_organization_by_name(o1.name))
        self.assertIsNotNone(get_organization_by_name(o2.name))
        self.assertIsNotNone(get_organization_by_name(o3.name))

        self.assertEqual(get_organization_by_name(o1.name), o1)
        self.assertEqual(get_organization_by_name(o2.name), o2)
        self.assertEqual(get_organization_by_name(o3.name), o3)

        self.assertIsNone(get_organization_by_name("Apple"))
        self.assertIsNone(get_organization_by_name("IBM"))
        self.assertIsNone(get_organization_by_name("Cisco"))

        self.assertNotEqual(get_organization_by_name("Apple"), o1)
        self.assertNotEqual(get_organization_by_name("IBM"), o1)
        self.assertNotEqual(get_organization_by_name("Cisco"), o1)

        self.assertNotEqual(get_organization_by_name("Apple"), o2)
        self.assertNotEqual(get_organization_by_name("IBM"), o2)
        self.assertNotEqual(get_organization_by_name("Cisco"), o2)

        self.assertNotEqual(get_organization_by_name("Apple"), o3)
        self.assertNotEqual(get_organization_by_name("IBM"), o3)
        self.assertNotEqual(get_organization_by_name("Cisco"), o3)

    def test_get_organizations_ordered_by_name(self):

        o1 = Organization(name = "Google")
        o2 = Organization(name = "Yahoo")
        o3 = Organization(name = "Ubisoft")
        o4 = Organization(name = "IBM")
        o5 = Organization(name = "Cisco")

        o1.save()
        o2.save()
        o3.save()
        o4.save()
        o5.save()

        #test typical cases
        organization_list = get_organizations_ordered_by_name()
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
