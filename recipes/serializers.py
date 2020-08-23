from rest_framework.serializers import ModelSerializer, Serializer
from recipes.models import Recipe, IngredientAmount, Ingredient, Unit, Amount


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'plural']


class UnitSerializer(ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'name']

class AmountSerializer(ModelSerializer):
    unit = UnitSerializer()

    class Meta:
        model = Amount
        fields = ['quantity', 'unit']


class IngredientAmountSerializer(ModelSerializer):
    ingredient = IngredientSerializer()
    amount = AmountSerializer()

    class Meta:
        model = IngredientAmount
        fields = ['ingredient', 'amount']


class RecipeModelSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'servings', 'instructions', 'created']


class RecipeSerializer(Serializer):  # pylint: disable=abstract-method
    recipe = RecipeModelSerializer()
    ingredients = IngredientAmountSerializer(many=True, required=False)

    def create(self, validated_data):
        return Recipe.recipes.create(**validated_data)

    def update(self, instance, validated_data):
        return Recipe.recipes.update(instance, **validated_data)


class RecipeListSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'created']
