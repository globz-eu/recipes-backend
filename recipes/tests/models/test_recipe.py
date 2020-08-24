from datetime import datetime
from recipes.models import Recipe, IngredientAmount
from recipes.tests.helpers import get_recipe_data
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
        for name, value in recipe_data['recipe'].items():
            self.assertEqual(
                getattr(recipe, name),
                value
            )
        ingredient_set = recipe.ingredient_set.all()
        ingredient_amounts = [
            IngredientAmount.objects.select_related('amount').get(
                recipe=recipe,
                ingredient=ingredient
            ) for ingredient in ingredient_set
        ]
        for i, ingredient in enumerate(recipe_data['ingredients']):
            self.compare_object_values(ingredient_amounts[i], ingredient)


class RecipeGetTest(RecipeIngredients):

    def test_recipe_get(self):
        recipe_data = get_recipe_data('lekker')
        recipe, ingredients = Recipe.recipes.get(pk=self.lekker.pk)
        self.compare_object_values(recipe, recipe_data['recipe'])
        for i, ingredient in enumerate(recipe_data['ingredients']):
            self.compare_object_values(ingredients[i], ingredient)
