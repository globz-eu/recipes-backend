from recipes.tests.helpers import get_recipe_data
from recipes.tests.views import status, reverse, InitializeRecipes, Authenticate


class GetSingleRecipeTest(InitializeRecipes, Authenticate):
    """ Test getting a single recipe """

    def setUp(self):
        InitializeRecipes.setUp(self)
        Authenticate.setUp(self)
        self.recipe_data = get_recipe_data('lekker')

    def test_get_valid_single_recipe(self):
        response = self.client.get(
            reverse('recipe_detail', kwargs={'pk': self.lekker.pk}))
        self.compare_values(response.data['recipe'], self.recipe_data['recipe'])
        for i, ingredient in enumerate(self.recipe_data['ingredients']):
            self.compare_values(response.data['ingredients'][i], ingredient)

    def test_get_invalid_single_recipe(self):
        response = self.client.get(
            reverse('recipe_detail', kwargs={'pk': 3000}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetSingleRecipeUnauthenticatedTest(InitializeRecipes):
    """ Test getting a single recipe without authentication """

    def test_get_valid_single_recipe(self):
        response = self.client.get(
            reverse('recipe_detail', kwargs={'pk': self.lekker.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_invalid_single_recipe(self):
        response = self.client.get(
            reverse('recipe_detail', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
