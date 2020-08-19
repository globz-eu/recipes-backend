from django.test import TestCase
from recipes.models import Recipe
from recipes.tests.helpers import get_recipe_data


class RecipeIngredients(TestCase):

    def setUp(self):
        recipe_data = get_recipe_data('lekker')
        self.lekker = Recipe.recipes.create(**recipe_data)
