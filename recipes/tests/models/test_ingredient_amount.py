from recipes.tests.helpers import get_recipe_data, get_ingredient_amounts
from recipes.tests.models.setup import RecipeIngredients


class IngredientAmountTest(RecipeIngredients):

    def test_db_fields(self):
        recipe_data = get_recipe_data('lekker')
        ingredient_amounts = get_ingredient_amounts(self.lekker)
        for i, ingredient in enumerate(recipe_data['ingredients']):
            self.compare_object_values(ingredient_amounts[i], ingredient)
