from recipes.models import IngredientAmount
from recipes.tests.helpers import get_recipe_data
from recipes.tests.models.setup import RecipeIngredients


class IngredientAmountTest(RecipeIngredients):

    def test_db_fields(self):
        recipe_data = get_recipe_data('lekker')
        ingredient_set = self.lekker.ingredient_set.all()
        for i, ingredient in enumerate(recipe_data['ingredients']):
            for name, value in ingredient['ingredient'].items():
                self.assertEqual(getattr(ingredient_set[i], name), value)
            ingredient_amount = IngredientAmount.objects.select_related('amount').get(
                recipe=self.lekker,
                ingredient=ingredient_set[i]
            )
            self.assertEqual(
                ingredient_amount.amount.unit.name,
                ingredient['amount']['unit']['name']
            )
            self.assertEqual(ingredient_amount.amount.quantity, ingredient['amount']['quantity'])
