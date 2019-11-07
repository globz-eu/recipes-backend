from django.test import TestCase
from ..models import Recipe


class RecipeTest(TestCase):
    """ Test module for Recipe model """


    def setUp(self):
        Recipe.objects.create(name='Lekker', for_persons=3, instructions='Stir well')

    def test_db_fields(self):
        recipe_lekker = Recipe.objects.get(name='Lekker')
        self.assertEqual(recipe_lekker.instructions, 'Stir well')
        self.assertEqual(recipe_lekker.for_persons, 3)
