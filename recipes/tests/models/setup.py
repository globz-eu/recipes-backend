from recipes.models import Recipe
from recipes.tests.helpers import get_recipe_data
from recipes.tests.views.setup import RecipeCompare


class RecipeIngredients(RecipeCompare):

    def setUp(self):
        recipe_data = get_recipe_data('lekker')
        self.lekker = Recipe.recipes.create(**recipe_data)
