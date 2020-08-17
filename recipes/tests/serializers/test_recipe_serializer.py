from recipes.models import Recipe
from recipes.serializers import RecipeModelSerializer, RecipeSerializer
from recipes.tests.helpers import get_ingredient_amounts, get_recipe_data
from recipes.tests.models.setup import RecipeIngredients


class RecipeModelSerializerTest(RecipeIngredients):
    def test_serializer(self):
        recipe = Recipe.objects.get(pk=self.lekker.pk)
        serializer = RecipeModelSerializer(recipe)
        self.assertEqual(serializer.data['id'], recipe.pk)
        self.assertEqual(serializer.data['name'], recipe.name)
        self.assertEqual(serializer.data['servings'], recipe.servings)
        self.assertEqual(serializer.data['instructions'], recipe.instructions)
        # self.assertEqual(serializer.data['created'], recipe.created)


class RecipeSerializerTest(RecipeIngredients):
    def test_serializer(self):
        recipe, ingredient_amounts = Recipe.recipes.get(pk=self.lekker.pk)
        serializer = RecipeSerializer(dict(recipe=recipe, ingredient_amounts=ingredient_amounts))
        self.assertEqual(serializer.data['recipe']['name'], 'Lekker')
        self.assertEqual(serializer.data['recipe']['id'], self.lekker.pk)
        self.assertEqual(
            serializer.data['ingredient_amounts'][0]['ingredient']['name'],
            'aubergine'
        )
        self.assertEqual(
            serializer.data['ingredient_amounts'][0]['ingredient']['id'],
            ingredient_amounts[0].ingredient.id
        )
        self.assertEqual(
            serializer.data['ingredient_amounts'][0]['unit']['name'],
            'piece'
        )

    def test_data_serializer(self):
        recipe_data = get_recipe_data('frozen_pizza')
        serializer = RecipeSerializer(
            data=recipe_data
        )
        self.assertTrue(serializer.is_valid())
        self.assertEqual(
            serializer.validated_data['recipe']['instructions'],
            recipe_data['recipe']['instructions']
        )
        self.assertEqual(
            serializer.validated_data['ingredient_amounts'][0]['quantity'],
            recipe_data['ingredient_amounts'][0]['quantity']
        )
        self.assertEqual(
            serializer.validated_data['ingredient_amounts'][0]['ingredient']['name'],
            recipe_data['ingredient_amounts'][0]['ingredient']['name']
        )
        self.assertEqual(
            serializer.validated_data['ingredient_amounts'][0]['unit']['name'],
            recipe_data['ingredient_amounts'][0]['unit']['name']
        )

    def test_serializer_create(self):
        recipe_data = get_recipe_data('frozen_pizza')
        serializer = RecipeSerializer(
            data=recipe_data
        )
        self.assertTrue(serializer.is_valid())
        recipe = serializer.save()
        ingredient_amounts = get_ingredient_amounts(recipe)
        self.assertEqual(recipe.instructions, recipe_data['recipe']['instructions'])
        self.assertEqual(
            ingredient_amounts[0].ingredient.name,
            recipe_data['ingredient_amounts'][0]['ingredient']['name']
        )
