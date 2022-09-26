# Generated by Django 3.2.6 on 2022-09-26 13:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favorite',
            options={'verbose_name': 'Избранное', 'verbose_name_plural': 'Избранное'},
        ),
        migrations.AlterModelOptions(
            name='ingredientamount',
            options={'verbose_name': 'Количество ингредиента', 'verbose_name_plural': 'Количество ингредиентов'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-pub_date'], 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterModelOptions(
            name='shoppinglist',
            options={'verbose_name': 'Покупка', 'verbose_name_plural': 'Покупки'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'Тэг', 'verbose_name_plural': 'Тэги'},
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='measurement_unit',
            field=models.CharField(max_length=20, verbose_name='Единицы измерения'),
        ),
        migrations.AlterField(
            model_name='ingredientamount',
            name='amount',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(0.001)], verbose_name='Количество ингредиентов'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=20, unique=True, verbose_name='Название тега'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('recipe', 'user'), name='favorite_recipe_user_unique'),
        ),
        migrations.AddConstraint(
            model_name='shoppinglist',
            constraint=models.UniqueConstraint(fields=('recipe', 'user'), name='shopping_list_recipe_user_unique'),
        ),
    ]