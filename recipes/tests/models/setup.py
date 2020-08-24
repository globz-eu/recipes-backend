from decimal import Decimal
from django.test import TestCase
from recipes.models import Recipe
from recipes.tests.helpers import get_recipe_data


class RecipeCompare(TestCase):

    def compare_values(self, returned, expected):
        for name, value in expected.items():
            if isinstance(value, dict):
                self.compare_values(returned[name], value)
            elif isinstance(value, int):
                self.assertEqual(int(Decimal(returned[name])), value)
            else:
                self.assertEqual(returned[name], value)

    def compare_object_values(self, returned, expected):
        for name, value in expected.items():
            if isinstance(value, dict):
                self.compare_object_values(getattr(returned, name), value)
            elif isinstance(value, int):
                self.assertEqual(int(Decimal(getattr(returned, name))), value)
            else:
                self.assertEqual(getattr(returned, name), value)


class RecipeIngredients(RecipeCompare):

    def setUp(self):
        recipe_data = get_recipe_data('lekker')
        self.lekker = Recipe.recipes.create(**recipe_data)
