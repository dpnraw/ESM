from django.test import TestCase

from .models import EggType


class EggTypeTest(TestCase):

    def setUp(self):

        EggType.objects.create(type='M+', price='100')

    def test_egg_type_name(self):
        egg_type = EggType.objects.latest('id')
        self.assertEqual(egg_type.type, 'M+')
        self.assertEqual(egg_type.price, 100)
