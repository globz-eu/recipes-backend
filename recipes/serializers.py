from rest_framework.serializers import ModelSerializer, Serializer
from recipes.models import Recipe, IngredientAmount, Ingredient, Unit


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'plural']


class UnitSerializer(ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'name']


class IngredientAmountSerializer(ModelSerializer):
    ingredient = IngredientSerializer()
    unit = UnitSerializer()

    class Meta:
        model = IngredientAmount
        fields = ['ingredient', 'unit', 'quantity']


class RecipeModelSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'servings', 'instructions', 'created']


class RecipeSerializer(Serializer):  # pylint: disable=abstract-method
    recipe = RecipeModelSerializer()
    ingredient_amounts = IngredientAmountSerializer(many=True)

    def create(self, validated_data):
        return Recipe.recipes.create(**validated_data)


class RecipeListSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'created']
