from decimal import Decimal
from recipes.models import Recipe, IngredientAmount
from recipes.serializers import IngredientAmountSerializer
from recipes.tests.helpers import get_ingredient_amounts, get_recipe_data
from recipes.tests.models.setup import RecipeIngredients


class IngredientAmountSerializerTest(RecipeIngredients):
    def test_single_serializer(self):
        ingredient_amounts = get_ingredient_amounts(self.lekker)
        ingredient_amount = IngredientAmount.objects.get(
            recipe=self.lekker,
            ingredient=ingredient_amounts[1].ingredient
        )
        serializer = IngredientAmountSerializer(ingredient_amount)
        self.assertEqual(serializer.data['unit']['name'], 'piece')
        self.assertEqual(serializer.data['ingredient']['name'], 'garlic')
        self.assertEqual(Decimal(serializer.data['quantity']), 1)

    def test_multiple_serializer(self):
        recipe = Recipe.objects.get(pk=self.lekker.pk)
        ingredient_amounts = get_ingredient_amounts(recipe)
        serializer = IngredientAmountSerializer(ingredient_amounts, many=True)
        self.assertEqual(serializer.data[1]['unit']['name'], 'piece')
        self.assertEqual(serializer.data[1]['ingredient']['name'], 'garlic')
        self.assertEqual(Decimal(serializer.data[1]['quantity']), 1)

    def test_data_serializer(self):
        recipe_data = get_recipe_data('frozen_pizza')
        ingredient_amount = recipe_data['ingredient_amounts'][0]
        serializer = IngredientAmountSerializer(data=ingredient_amount)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(
            serializer.validated_data['unit']['name'],
            ingredient_amount['unit']['name']
        )
        self.assertEqual(
            serializer.validated_data['ingredient']['name'],
            ingredient_amount['ingredient']['name']
        )
        self.assertEqual(
            Decimal(serializer.validated_data['quantity']),
            ingredient_amount['quantity']
        )
