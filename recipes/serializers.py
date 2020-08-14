from rest_framework.serializers import ModelSerializer, Serializer
from recipes.models import Recipe, IngredientAmount


class IngredientAmountSerializer(ModelSerializer):
    class Meta:
        model = IngredientAmount
        fields = ['ingredient', 'unit', 'quantity']
        depth = 1


class RecipeSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'servings', 'instructions', 'created']


class RecipeWithIngredientAmountsSerializer(Serializer):  # pylint: disable=abstract-method
    recipe = RecipeSerializer()
    ingredient_amounts = IngredientAmountSerializer(many=True)


class RecipeListSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'created']
