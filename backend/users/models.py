from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import UniqueConstraint


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
    USER = 'user'
    ADMIN = 'admin'
    ROLES = (
        (USER, 'user'),
        (ADMIN, 'admin')
    )

    role = models.CharField(
        verbose_name='Пользовательская роль',
        max_length=200,
        choices=ROLES,
        default='user'
    )

    email = models.EmailField(
        'email',
        null=False,
        unique=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyUserManager()

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']

    def __str__(self):
        return f'{self.username}'


class Follow(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписка',
        related_name='following'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='follower'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        UniqueConstraint(fields=['author', 'user'], name='follow_unique')

    def __str__(self):
        return f'{self.user} -> {self.author}'
