from datetime import datetime
from recipes.models import Recipe
from recipes.tests.helpers import get_recipe_data, get_ingredient_amounts
from recipes.tests.models.setup import RecipeIngredients, RecipeCompare


class RecipeTest(RecipeIngredients):

    def test_db_fields(self):
        recipe_data = get_recipe_data('lekker')
        self.compare_object_values(self.lekker, recipe_data['recipe'])
        self.assertIsInstance(self.lekker.created, datetime)


class RecipeCreateTest(RecipeCompare):

    def test_recipe_create(self):
        recipe_data = get_recipe_data('lekker')
        recipe = Recipe.recipes.create(**recipe_data)
        self.compare_object_values(recipe, recipe_data['recipe'])
        ingredient_amounts = get_ingredient_amounts(recipe)
        for i, ingredient in enumerate(recipe_data['ingredients']):
            self.compare_object_values(ingredient_amounts[i], ingredient)


class RecipeGetTest(RecipeIngredients):

    def test_recipe_get(self):
        recipe_data = get_recipe_data('lekker')
        recipe, ingredients = Recipe.recipes.get(pk=self.lekker.pk)
        self.compare_object_values(recipe, recipe_data['recipe'])
        for i, ingredient in enumerate(recipe_data['ingredients']):
            self.compare_object_values(ingredients[i], ingredient)
