import json
from recipes.tests.helpers import get_recipe_data
from recipes.tests.views import status, reverse, InitializeRecipes, Authenticate, Recipe
from . import RecipeModelSerializer


class UpdateSingleRecipeTest(InitializeRecipes, Authenticate):
    """ Test updating an existing recipe """

    def setUp(self):
        InitializeRecipes.setUp(self)
        Authenticate.setUp(self)
        self.recipe_data = get_recipe_data('lekker')

    def test_valid_update_recipe(self):
        response = self.client.put(
            reverse('recipe_detail', kwargs={'pk': self.lekker.pk}),
            data=json.dumps(self.recipe_data['recipe']),
            content_type='application/json'
        )
        recipe = Recipe.objects.get(pk=self.lekker.pk)
        serializer = RecipeModelSerializer(recipe)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_recipe(self):
        response = self.client.put(
            reverse('recipe_detail', kwargs={'pk': self.pas_mal.pk}),
            data=json.dumps({}),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleRecipeUnauthenticatedTest(InitializeRecipes):
    """ Test updating an existing recipe without authentication """

    def setUp(self):
        InitializeRecipes.setUp(self)
        self.recipe_data = get_recipe_data('lekker')

    def test_valid_update_recipe(self):
        response = self.client.put(
            reverse('recipe_detail', kwargs={'pk': self.lekker.pk}),
            data=json.dumps(self.recipe_data['recipe']),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_update_recipe(self):
        response = self.client.put(
            reverse('recipe_detail', kwargs={'pk': self.pas_mal.pk}),
            data=json.dumps({}),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
