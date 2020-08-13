from django.test import TestCase
from recipes.models import Unit


class UnitTest(TestCase):

    def setUp(self):
        Unit.objects.create(name='mililiter')

    def test_db_fields(self):
        aubergine = Unit.objects.get(name='mililiter')
        self.assertEqual(aubergine.name, 'mililiter')
