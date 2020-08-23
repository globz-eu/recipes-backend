from decimal import Decimal
from recipes.models import  IngredientAmount
from recipes.serializers import IngredientAmountSerializer
from recipes.tests.helpers import get_recipe_data
from recipes.tests.models.setup import RecipeIngredients


class IngredientAmountSerializerTest(RecipeIngredients):
    def test_single_serializer(self):
        recipe_data = get_recipe_data('lekker')
        ingredient_set = self.lekker.ingredient_set.all()
        for i, ingredient in enumerate(recipe_data['ingredients']):
            ingredient_amount = IngredientAmount.objects.select_related('amount').get(
                recipe=self.lekker,
                ingredient=ingredient_set[i]
            )
            serializer = IngredientAmountSerializer(ingredient_amount)
            for name, value in ingredient['ingredient'].items():
                self.assertEqual(serializer.data['ingredient'][name], value)
            self.assertEqual(
                serializer.data['amount']['unit']['name'],
                ingredient['amount']['unit']['name']
            )
            self.assertEqual(
                Decimal(serializer.data['amount']['quantity']),
                ingredient['amount']['quantity']
            )

    def test_multiple_serializer(self):
        recipe_data = get_recipe_data('lekker')
        ingredient_set = self.lekker.ingredient_set.all()
        ingredient_amounts = [
            IngredientAmount.objects.select_related('amount').get(
                recipe=self.lekker,
                ingredient=ingredient
            ) for ingredient in ingredient_set
        ]
        serializer = IngredientAmountSerializer(ingredient_amounts, many=True)
        for i, ingredient in enumerate(recipe_data['ingredients']):
            for name, value in ingredient['ingredient'].items():
                self.assertEqual(serializer.data[i]['ingredient'][name], value)
            self.assertEqual(
                serializer.data[i]['amount']['unit']['name'],
                ingredient['amount']['unit']['name']
            )
            self.assertEqual(
                Decimal(serializer.data[i]['amount']['quantity']),
                ingredient['amount']['quantity']
            )

    def test_data_serializer(self):
        recipe_data = get_recipe_data('frozen_pizza')
        ingredient_amount = recipe_data['ingredients']
        serializer = IngredientAmountSerializer(data=ingredient_amount, many=True)
        self.assertTrue(serializer.is_valid())
        for i, ingredient in enumerate(recipe_data['ingredients']):
            for name, value in ingredient['ingredient'].items():
                self.assertEqual(serializer.validated_data[i]['ingredient'][name], value)
            self.assertEqual(
                serializer.validated_data[i]['amount']['unit']['name'],
                ingredient['amount']['unit']['name']
            )
            self.assertEqual(
                Decimal(serializer.validated_data[i]['amount']['quantity']),
                ingredient['amount']['quantity']
            )
