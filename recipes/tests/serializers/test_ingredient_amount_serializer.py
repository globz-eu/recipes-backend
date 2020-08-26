from recipes.serializers import IngredientAmountSerializer
from recipes.tests.helpers import get_recipe_data, get_ingredient_amounts
from recipes.tests.models.setup import RecipeIngredients


class IngredientAmountSerializerTest(RecipeIngredients):
    def test_single_serializer(self):
        recipe_data = get_recipe_data('lekker')
        ingredient_amounts = get_ingredient_amounts(self.lekker)
        for i, ingredient in enumerate(recipe_data['ingredients']):
            serializer = IngredientAmountSerializer(ingredient_amounts[i])
            self.compare_values(serializer.data, ingredient)

    def test_multiple_serializer(self):
        recipe_data = get_recipe_data('lekker')
        ingredient_amounts = get_ingredient_amounts(self.lekker)
        serializer = IngredientAmountSerializer(ingredient_amounts, many=True)
        for i, ingredient in enumerate(recipe_data['ingredients']):
            self.compare_values(serializer.data[i], ingredient)

    def test_data_serializer(self):
        recipe_data = get_recipe_data('frozen_pizza')
        ingredient_amount = recipe_data['ingredients']
        serializer = IngredientAmountSerializer(data=ingredient_amount, many=True)
        self.assertTrue(serializer.is_valid())
        for i, ingredient in enumerate(recipe_data['ingredients']):
            self.compare_values(serializer.validated_data[i], ingredient)
