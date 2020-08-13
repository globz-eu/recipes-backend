from django.db import models


class Recipe(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    servings = models.PositiveSmallIntegerField(default=4)
    instructions = models.TextField(max_length=1000)

    class Meta:
        ordering = ['name']


class Ingredient(models.Model):
    recipes = models.ManyToManyField(Recipe)
    name = models.CharField(max_length=100)
    plural = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']
