from django.db import models

from users.models import User


class Tag(models.Model):
    """Модель для установки Тэгов."""

    name = models.CharField(
        'Тэг',
        max_length=200
    )
    color = models.CharField(
        'Цвет',
        max_length=7
    )
    slug = models.SlugField(
        'Слэг',
        max_length=200,
        unique=True
    )
    recipe = models.ForeignKey(
        'Recipe',
        verbose_name='рецепты',
        help_text='Рецепт, к которой будет относиться tag',
        blank=True,
        null=True,
        related_name='tags',
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    """Модель для установки Тэгов."""

    name = models.ManyToManyField(
        'Recipe',
        through='RecipeIngredients'
    )
    measurement_unit = models.CharField(
        'Единицы измерения',
        max_length=200
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель для работы с рецептами."""

    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    name = models.TextField(
        'Название рецепта',
    )
    image = models.ImageField(
        'Картинка',
        upload_to='images/',
        null=True,
        default=None
    )
    text = models.TextField(
        'Текстовое описание',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время готовки',
    )

    is_favorited = models.BooleanField(default=False)
    is_in_shopping_cart = models.BooleanField(default=False)
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    ingredients = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.recipe} {self.ingredients}'


