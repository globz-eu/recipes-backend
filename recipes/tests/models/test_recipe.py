from recipes.models import Recipe
from recipes.tests.models.setup import RecipeIngredients


class RecipeTest(RecipeIngredients):

    def test_db_fields(self):
        expected_ingredients = ['aubergine', 'garlic']
        lekker = Recipe.objects.get(name='Lekker')
        ingredients = lekker.ingredient_amounts.all()
        self.assertEqual(lekker.name, 'Lekker')
        self.assertEqual(lekker.instructions, 'Stir well')
        self.assertEqual(lekker.servings, 3)
        for i, ingredient in enumerate(ingredients):
            self.assertEqual(ingredient.name, expected_ingredients[i])
