import json
from recipes.models import Recipe
from recipes.tests.helpers import get_recipe_data
from recipes.tests.views import status, reverse, InitializeRecipes, Authenticate


class UpdateSingleRecipeTest(InitializeRecipes, Authenticate):
    """ Test updating an existing recipe """

    def setUp(self):
        InitializeRecipes.setUp(self)
        Authenticate.setUp(self)
        self.recipe_data = get_recipe_data('lekker')
        self.recipe_data['recipe']['instructions'] = "Stir well for 20 minutes"
        self.recipe_data['ingredients'][1]['ingredient']['name'] = "onion"
        self.recipe_data['ingredients'][1]['ingredient']['plural'] = "onions"
        self.recipe_data['ingredients'][0]['amount']['quantity'] = 3

    def test_valid_update_recipe(self):
        response = self.client.put(
            reverse('recipe_detail', kwargs={'pk': self.lekker.pk}),
            data=json.dumps(self.recipe_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.compare_values(response.data['recipe'], self.recipe_data['recipe'])
        for i, ingredient in enumerate(self.recipe_data['ingredients']):
            self.compare_values(response.data['ingredients'][i], ingredient)

    def test_updates_recipe_in_database(self):
        self.client.put(
            reverse('recipe_detail', kwargs={'pk': self.lekker.pk}),
            data=json.dumps(self.recipe_data),
            content_type='application/json'
        )
        recipe, ingredient_amounts = Recipe.recipes.get(pk=self.lekker.pk)
        self.compare_object_values(recipe, self.recipe_data['recipe'])
        for i, ingredient in enumerate(self.recipe_data['ingredients']):
            self.compare_object_values(ingredient_amounts[i], ingredient)

    def test_invalid_update_recipe(self):
        response = self.client.put(
            reverse('recipe_detail', kwargs={'pk': self.lekker.pk}),
            data=json.dumps({}),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleRecipeUnauthenticatedTest(InitializeRecipes):
    """ Test updating an existing recipe without authentication """

    def setUp(self):
        InitializeRecipes.setUp(self)
        self.recipe_data = get_recipe_data('lekker')
        self.recipe_data['recipe']['instructions'] = "Stir well for 20 minutes"
        self.recipe_data['ingredients'][1]['ingredient']['name'] = "onion"
        self.recipe_data['ingredients'][1]['ingredient']['plural'] = "onions"
        self.recipe_data['ingredients'][0]['amount']['quantity'] = 3

    def test_valid_update_recipe(self):
        response = self.client.put(
            reverse('recipe_detail', kwargs={'pk': self.lekker.pk}),
            data=json.dumps(self.recipe_data['recipe']),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_update_recipe(self):
        response = self.client.put(
            reverse('recipe_detail', kwargs={'pk': self.lekker.pk}),
            data=json.dumps({}),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
