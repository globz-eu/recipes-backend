import os
from decimal import Decimal
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from recipes.models import Recipe
from recipes.tests.helpers import get_recipe_data, check_values


class RecipeCompare(APITestCase):

    def assertion(self, returned, expected):
        if isinstance(expected, int):
            self.assertEqual(int(Decimal(returned)), expected)
        else:
            self.assertEqual(returned, expected)

    def compare_values(self, returned, expected):
        check_values(returned, expected, self.assertion)

    def compare_object_values(self, returned, expected):
        check_values(returned, expected, self.assertion, returned_is_object=True)


class InitializeRecipes(RecipeCompare):
    """ Initialize 2 recipes """

    def setUp(self):
        recipe_data = get_recipe_data('lekker')
        self.lekker = Recipe.recipes.create(**recipe_data)
        self.pas_mal = Recipe.objects.create(
            name='Pas mal',
            servings=2,
            instructions='Servir sur un lit de choucroute'
        )


class Authenticate(RecipeCompare):
    def setUp(self):
        self.user = User.objects.get(username=os.environ['AUTH0_USERNAME'])
        self.client.force_authenticate(user=self.user) # pylint: disable=no-member

    def tearDown(self):
        self.client.force_authenticate(user=None) # pylint: disable=no-member
