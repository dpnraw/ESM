from django.test import TestCase

from .models import Customer


class CustomerTest(TestCase):

    def setUp(self):
        Customer.objects.create(name='Test User', location='28.96,86.45')

    def test_attrs(self):
        customer = Customer.objects.latest('id')
        self.assertEqual(customer.name, 'Test User')
        # Location becomes tuple of latitude and longitude.
        self.assertEqual(customer.location, (28.96, 86.45))
