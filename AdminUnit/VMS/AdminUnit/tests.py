from django.test import TestCase

# Create your tests here.
class SimpleTest(TestCase):
	def test_index(self):
		resp = self.client.get('/AdminUnit/')
		self.assertEqual(resp.status_code,200)
