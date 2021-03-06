import json
from rest_framework.test import APITestCase
from recipes.tests.helpers import get_recipe_data_flat
from recipes.tests.views import reverse, status, Authenticate


class CreateNewRecipeTest(Authenticate):
    """ Test creating a new recipe """

    def setUp(self):
        Authenticate.setUp(self)
        self.recipe_data, self.expected_recipe = get_recipe_data_flat('lekker')

    def test_create_valid_recipe(self):
        response = self.client.post(
            reverse('recipes'),
            data=json.dumps(self.expected_recipe),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.compare_values(response.data, self.expected_recipe)

    def test_create_valid_recipe_with_ingredients(self):
        response = self.client.post(
            reverse('recipes'),
            data=json.dumps(self.recipe_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.compare_values(response.data, self.expected_recipe)
        for i, ingredient in enumerate(self.recipe_data['ingredients']):
            self.compare_values(response.data['ingredients'][i], ingredient)

    def test_create_invalid_recipe(self):
        response = self.client.post(
            reverse('recipes'),
            data=json.dumps(dict(recipe={})),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CreateNewRecipeUnauthenticatedTest(APITestCase):
    """ Test creating a new recipe without authentication """

    def setUp(self):
        self.recipe_data, self.expected_recipe = get_recipe_data_flat('lekker')

    def test_create_valid_recipe(self):
        response = self.client.post(
            reverse('recipes'),
            data=json.dumps(dict(recipe=self.recipe_data)),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_invalid_recipe(self):
        response = self.client.post(
            reverse('recipes'),
            data=json.dumps(dict(recipe={})),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
