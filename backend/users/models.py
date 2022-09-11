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
    SUBSCRIBED = 'subscribed'
    ADMIN = 'admin'
    ROLES = (
        (USER, 'user'),
        (SUBSCRIBED, 'subscribed'),
        (ADMIN, 'admin')
    )
    role = models.CharField(
        verbose_name='Пользовательская роль',
        max_length=200,
        choices=ROLES,
        default='user'
    )

    objects = MyUserManager()

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_subscribed(self):
        return self.role == self.SUBSCRIBED

    class Meta:
        ordering = ('id',)


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
