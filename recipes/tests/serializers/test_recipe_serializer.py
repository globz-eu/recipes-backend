from recipes.models import Recipe, IngredientAmount, Ingredient
from recipes.serializers import RecipeModelSerializer, RecipeSerializer, IngredientAmountSerializer
from recipes.tests.models.setup import RecipeIngredients


class RecipeSerializerTest(RecipeIngredients):
    def test_serializer(self):
        recipe = Recipe.objects.get(pk=self.lekker.pk)
        serializer = RecipeModelSerializer(recipe)
        self.assertEqual(serializer.data['id'], recipe.pk)
        self.assertEqual(serializer.data['name'], recipe.name)
        self.assertEqual(serializer.data['servings'], recipe.servings)
        self.assertEqual(serializer.data['instructions'], recipe.instructions)
        # self.assertEqual(serializer.data['created'], recipe.created)


class IngredientAmountSerializerTest(RecipeIngredients):
    def test_single_serializer(self):
        ingredient_amount = IngredientAmount.objects.get(
            recipe=self.lekker,
            ingredient=self.garlic
        )
        serializer = IngredientAmountSerializer(ingredient_amount)
        self.assertEqual(serializer.data['unit']['name'], 'piece')
        self.assertEqual(serializer.data['ingredient']['name'], 'garlic')

    def test_multiple_serializer(self):
        recipe = Recipe.objects.get(pk=self.lekker.pk)
        ingredient_ids = [ingredient.pk for ingredient in recipe.ingredient_amounts.all()]
        ingredients = Ingredient.objects.filter(pk__in=ingredient_ids)
        ingredient_amounts = IngredientAmount.objects.filter(
            recipe=self.lekker,
            ingredient__in=ingredients
        )
        ingredient_amounts_serializer = IngredientAmountSerializer(ingredient_amounts, many=True)
        self.assertEqual(ingredient_amounts_serializer.data[1]['unit']['name'], 'piece')


class RecipeWithIngredientAmountsSerializerTest(RecipeIngredients):
    def test_serializer(self):
        recipe = Recipe.objects.get(pk=self.lekker.pk)
        ingredient_ids = [ingredient.pk for ingredient in recipe.ingredient_amounts.all()]
        ingredients = Ingredient.objects.filter(pk__in=ingredient_ids)
        ingredient_amounts = IngredientAmount.objects.filter(
            recipe=self.lekker,
            ingredient__in=ingredients
        )
        recipe_with_ingredient_amounts = dict(recipe=recipe, ingredient_amounts=ingredient_amounts)
        serializer = RecipeSerializer(recipe_with_ingredient_amounts)
        self.assertEqual(serializer.data['recipe']['name'], 'Lekker')
        self.assertEqual(
            serializer.data['ingredient_amounts'][0]['ingredient']['name'],
            'aubergine'
        )
        self.assertEqual(
            serializer.data['ingredient_amounts'][0]['unit']['name'],
            'piece'
        )
