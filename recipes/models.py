from django.db import models


class RecipeManager(models.Manager):
    def get(self, **kwargs):
        recipe = self.model.objects.get(**kwargs)
        ingredient_set = recipe.ingredient_set.all()
        ingredients = IngredientAmount.objects.filter(
            recipe=recipe,
            ingredient__in=ingredient_set
        ).order_by('ingredient').select_related('amount', 'ingredient')
        return recipe, ingredients

    def create(self, recipe, ingredients=None):
        new_recipe = self.model(
            name=recipe['name'],
            servings=recipe['servings'],
            instructions=recipe['instructions']
        )
        new_recipe.save()
        if ingredients:
            for ingredient in ingredients:
                ingredient_object, _ = Ingredient.objects.get_or_create(
                    name=ingredient['ingredient']['name'],
                    plural=ingredient['ingredient']['plural']
                )
                unit, _ = Unit.objects.get_or_create(name=ingredient['amount']['unit']['name'])
                amount, _ = Amount.objects.get_or_create(
                    quantity=ingredient['amount']['quantity'],
                    unit=unit
                )
                ingredient_object.recipes.add(
                    new_recipe,
                    through_defaults={
                        'amount': amount
                    }
                )
        return new_recipe

    def update(self, instance, recipe, ingredients=None):  # pylint: disable=no-self-use
        instance.name = recipe['name']
        instance.servings = recipe['servings']
        instance.instructions = recipe['instructions']
        instance.save()

        if ingredients:
            instance.ingredient_set.clear()
            for ingredient in ingredients:
                ingredient_object, _ = Ingredient.objects.update_or_create(
                    name=ingredient['ingredient']['name'],
                    plural=ingredient['ingredient']['plural']
                )
                unit, _ = Unit.objects.update_or_create(name=ingredient['amount']['unit']['name'])
                amount, _ = Amount.objects.update_or_create(
                    quantity=ingredient['amount']['quantity'],
                    unit=unit
                )
                instance.ingredient_set.add(ingredient_object, through_defaults={'amount': amount})

        return instance


class Recipe(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    servings = models.PositiveSmallIntegerField(default=4)
    instructions = models.TextField(max_length=1000)

    objects = models.Manager()
    recipes = RecipeManager()

    class Meta:
        ordering = ['name']
        constraints = [models.UniqueConstraint(fields=['name'], name='unique_recipe_name')]


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    plural = models.CharField(max_length=100)
    recipes = models.ManyToManyField(Recipe, through='IngredientAmount')

    class Meta:
        ordering = ['name']
        constraints = [models.UniqueConstraint(fields=['name'], name='unique_ingredient_name')]


class Unit(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']
        constraints = [models.UniqueConstraint(fields=['name'], name='unique_unit_name')]


class Amount(models.Model):
    quantity = models.DecimalField(max_digits=4, decimal_places=2)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.ForeignKey(Amount, on_delete=models.CASCADE, default=None)
