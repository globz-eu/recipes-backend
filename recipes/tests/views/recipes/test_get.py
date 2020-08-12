from recipes.serializers import RecipeListSerializer
from .. import reverse, status, InitializeRecipes, Authenticate, Recipe


class GetAllRecipesTest(InitializeRecipes, Authenticate):
    """ Test getting all recipes """

    def setUp(self):
        InitializeRecipes.setUp(self)
        Authenticate.setUp(self)

    def test_get_all_recipes(self):
        response = self.client.get(reverse('recipes'))
        recipes = Recipe.objects.all()
        serializer = RecipeListSerializer(recipes, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetAllRecipesAsUnauthenticatedTest(InitializeRecipes):
    """ Test getting all recipes without authentication """

    def test_get_all_recipes(self):
        response = self.client.get(reverse('recipes'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
