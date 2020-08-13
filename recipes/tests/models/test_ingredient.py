from django.test import TestCase
from recipes.models import Ingredient


class IngredientTest(TestCase):

    def setUp(self):
        Ingredient.objects.create(name='aubergine', plural='aubergines')

    def test_db_fields(self):
        aubergine = Ingredient.objects.get(name='aubergine')
        self.assertEqual(aubergine.plural, 'aubergines')
