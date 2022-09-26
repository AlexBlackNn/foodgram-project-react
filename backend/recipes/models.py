from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=20,
        verbose_name='Название тега',
        null=False,
        unique=True
    )
    slug = models.SlugField(
        verbose_name='Ссылка',
        unique=True,
        help_text='Ссылка тега'
    )
    color = models.CharField(
        max_length=7,
        default='#0Сffff',
        unique=True,
        verbose_name='Цвет тэга'
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ингредиенты для рецепта."""

    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента',
        null=False
    )
    measurement_unit = models.CharField(
        max_length=20,
        verbose_name='Единицы измерения',
        null=False
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} -> {self.measurement_unit}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='ingredients',
        through='IngredientAmount',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag, related_name='tags',
        verbose_name='Хэштег'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    text = models.TextField(
        verbose_name='Описание',
        max_length=1000
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        null=False
    )
    image = models.ImageField(
        upload_to='images/',
        verbose_name='Изображение'
    )
    cooking_time = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1, 'Значение не может быть меньше 1')],
        verbose_name='Время готовки в минутах',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        related_name='favorites',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='favorites',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='favorite_recipe_user_unique'
            )
        ]

    def __str__(self):
        return f'{self.user} -> {self.recipe.name}'


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_shopping_list',
        verbose_name='Пользоавтель'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='Покупка'
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='shopping_list_recipe_user_unique'
            )
        ]

    def __str__(self):
        return f'У пользователя {self.user} покупки: {self.recipe}'


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients_in_recipe',
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes_ingredients_list',
        verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(0.001)],
        verbose_name='Количество ингредиентов'
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        return f'{self.ingredient} {self.amount}  в рецепте {self.recipe}'
