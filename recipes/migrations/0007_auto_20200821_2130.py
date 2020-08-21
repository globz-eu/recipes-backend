# Generated by Django 3.0.8 on 2020-08-21 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_auto_20200815_1926'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='ingredient_amounts',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='recipes',
            field=models.ManyToManyField(through='recipes.IngredientAmount', to='recipes.Recipe'),
        ),
    ]
