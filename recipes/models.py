from django.db import models


class Recipe(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    for_persons = models.PositiveSmallIntegerField(default=4)
    instructions = models.TextField(max_length=1000)
