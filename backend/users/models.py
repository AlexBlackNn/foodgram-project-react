from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import MyUserManager


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
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'user'],
                name='follow_author_user_unique'
            )
        ]

    def __str__(self):
        return f'{self.user} -> {self.author}'
