from recipes.models import Recipe, IngredientAmount
from recipes.tests.models.setup import RecipeIngredients

class IngredientAmountTest(RecipeIngredients):

    def test_db_fields(self):
        expected_ingredients = [
            {'name': 'aubergine', 'quantity': 2, 'unit_name': 'piece'},
            {'name': 'garlic', 'quantity': 1, 'unit_name': 'piece'}
        ]
        lekker = Recipe.objects.get(name='Lekker')
        ingredients = lekker.ingredient_amounts.all()
        for i, ingredient in enumerate(ingredients):
            ingredient_amount = IngredientAmount.objects.get(
                recipe=lekker,
                ingredient=ingredient
            )
            self.assertEqual(ingredient.name, expected_ingredients[i]['name'])
            self.assertEqual(ingredient_amount.quantity, expected_ingredients[i]['quantity'])
            self.assertEqual(ingredient_amount.unit.name, expected_ingredients[i]['unit_name'])
