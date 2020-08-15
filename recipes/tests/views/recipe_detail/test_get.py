from recipes.helpers import get_ingredient_amounts
from . import RecipeSerializer
from .. import status, reverse, InitializeRecipes, Authenticate, Recipe


class GetSingleRecipeTest(InitializeRecipes, Authenticate):
    """ Test getting a single recipe """

    def setUp(self):
        InitializeRecipes.setUp(self)
        Authenticate.setUp(self)

    def test_get_valid_single_recipe(self):
        response = self.client.get(
            reverse('recipe_detail', kwargs={'pk': self.lekker.pk}))
        recipe = Recipe.objects.get(pk=self.lekker.pk)
        ingredient_amounts = get_ingredient_amounts(recipe)
        serializer = RecipeSerializer(dict(recipe=recipe, ingredient_amounts=ingredient_amounts))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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
