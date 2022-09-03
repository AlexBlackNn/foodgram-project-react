from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class MyUserManager(UserManager):
    """Для создания пользователя и суперпользователя."""

    def create_user(self, username, email, password, **extra_fields):
        return super().create_user(
            username, email=email, password=password, **extra_fields
        )

    def create_superuser(
            self, username, email, password, role='admin', **extra_fields):
        return super().create_superuser(
            username, email, password, role='admin', **extra_fields
        )


class User(AbstractUser):
    # пользовательские роли
    USER = 'user'
    AUTHORIZED = 'authorized'
    ADMIN = 'admin'
    ROLES = (
        (USER, 'user'),
        (AUTHORIZED, 'authorized'),
        (ADMIN, 'admin')
    )
    role = models.CharField(
        verbose_name='Пользовательская роль',
        max_length=200,
        choices=ROLES,
        default='user'
    )
    email = models.EmailField(unique=True, max_length=255)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        ordering = ('id',)


# Create your models here.


class Tag(models.Model):
    """Модель для установки Тэгов."""

    name = models.CharField(max_length=200)
    color = models.CharField(max_length=7)
    slug = models.SlugField(max_length=200, unique=True)

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

    name = models.ManyToManyField('Recipe', through='RecipeIngredients')
    measurement_unit = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель для работы с рецептами."""

    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='posts',
    )
    name = models.TextField(
        'Название рецепта',
        help_text='Название рецепта',
    )
    # Поле для картинок (необязательное)
    image = models.ImageField(
        'Картинка',
        upload_to='images/',
        blank=True
    )
    text = models.TextField(
        'Текстовое описание',
        help_text='Текстовое описание',
    )
    cooking_time = models.TextField(
        'Текст поста',
        help_text='Текст нового поста',
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
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredients = models.ForeignKey(Ingredients, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.recipe} {self.ingredients}'


class Follow(models.Model):
    """Класс для организации подписки на посты."""
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='follower',
    )

    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique subscription')
        ]
