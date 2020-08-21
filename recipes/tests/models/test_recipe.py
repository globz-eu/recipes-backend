from django.test import TestCase
from recipes.models import Recipe, IngredientAmount
from recipes.tests.helpers import get_ingredient_amounts, get_recipe_data
from recipes.tests.models.setup import RecipeIngredients


class RecipeTest(RecipeIngredients):

    def test_db_fields(self):
        recipe_data = get_recipe_data('lekker')
        ingredient_set = self.lekker.ingredient_set.all()
        for name, value in recipe_data['recipe'].items():
            self.assertEqual(
                getattr(self.lekker, name),
                value
            )
        for i, ingredient in enumerate(recipe_data['ingredients']):
            for name, value in ingredient['ingredient'].items():
                self.assertEqual(getattr(ingredient_set[i], name), value)
            ingredient_amount = IngredientAmount.objects.select_related('unit').get(
                recipe=self.lekker,
                ingredient=ingredient_set[i]
            )
            self.assertEqual(ingredient_amount.unit.name, ingredient['amount']['unit']['name'])
            self.assertEqual(ingredient_amount.quantity, ingredient['amount']['quantity'])


class RecipeCreateTest(TestCase):

    def test_recipe_create(self):
        recipe_data = get_recipe_data('lekker')
        recipe = Recipe.recipes.create(**recipe_data)
        self.assertEqual(recipe.name, recipe_data['recipe']['name'])
        self.assertEqual(recipe.servings, recipe_data['recipe']['servings'])
        self.assertEqual(recipe.instructions, recipe_data['recipe']['instructions'])
        ingredient_amounts = get_ingredient_amounts(recipe)
        self.assertEqual(
            ingredient_amounts[0].ingredient.name,
            recipe_data['ingredient_amounts'][0]['ingredient']['name']
        )
        self.assertEqual(
            ingredient_amounts[0].unit.name,
            recipe_data['ingredient_amounts'][0]['unit']['name']
        )
        self.assertEqual(
            ingredient_amounts[0].quantity,
            recipe_data['ingredient_amounts'][0]['quantity']
        )


class RecipeGetTest(RecipeIngredients):

    def test_recipe_get(self):
        recipe_data = get_recipe_data('lekker')
        recipe, ingredient_amounts = Recipe.recipes.get(pk=self.lekker.pk)
        self.assertEqual(recipe.name, recipe_data['recipe']['name'])
        self.assertEqual(
            ingredient_amounts[0].ingredient.name,
            recipe_data['ingredient_amounts'][0]['ingredient']['name']
        )
