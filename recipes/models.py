from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    plural = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']


class Recipe(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    servings = models.PositiveSmallIntegerField(default=4)
    instructions = models.TextField(max_length=1000)
    ingredient_amounts = models.ManyToManyField(Ingredient, through='IngredientAmount')

    class Meta:
        ordering = ['name']


class Unit(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=4, decimal_places=2)
