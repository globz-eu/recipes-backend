from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    plural = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']
        constraints = [models.UniqueConstraint(fields=['name'], name='unique_ingredient_name')]


class RecipeManager(models.Manager):  # pylint: disable = too-few-public-methods
    def create(self, recipe, ingredient_amounts):
        recipe = self.model(
            name=recipe['name'],
            servings=recipe['servings'],
            instructions=recipe['instructions']
        )
        recipe.save()
        for ingredient_amount in ingredient_amounts:
            ingredient, _ = Ingredient.objects.get_or_create(
                name=ingredient_amount['ingredient']['name'],
                plural=ingredient_amount['ingredient']['plural']
            )
            unit, _ = Unit.objects.get_or_create(name=ingredient_amount['unit']['name'])
            recipe.ingredient_amounts.add(
                ingredient,
                through_defaults={
                    'unit': unit,
                    'quantity': ingredient_amount['quantity']
                }
            )
        return recipe


class Recipe(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    servings = models.PositiveSmallIntegerField(default=4)
    instructions = models.TextField(max_length=1000)
    ingredient_amounts = models.ManyToManyField(Ingredient, through='IngredientAmount')
    objects = models.Manager()
    recipes = RecipeManager()

    class Meta:
        ordering = ['name']
        constraints = [models.UniqueConstraint(fields=['name'], name='unique_recipe_name')]


class Unit(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']
        constraints = [models.UniqueConstraint(fields=['name'], name='unique_unit_name')]


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=4, decimal_places=2)
