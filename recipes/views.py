from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer


@api_view(['GET', 'POST'])
def recipe_list(request, format=None):  # pylint: disable=redefined-builtin,unused-argument
    """
    List all recipes, or create a new recipe.
    """
    if request.method == 'GET':
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return None

@api_view(['GET', 'PUT', 'DELETE'])
def recipe_detail(request, pk, format=None):  # pylint: disable=redefined-builtin,invalid-name,unused-argument
    """
    Retrieve, update or delete a recipe.
    """
    try:
        recipe = Recipe.objects.get(pk=pk)
    except Recipe.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = RecipeSerializer(recipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return None
