from django.contrib.auth.models import UserManager


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
