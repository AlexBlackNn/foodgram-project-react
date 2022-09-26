from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Follow, User


@admin.register(User)
class UserAdmin(UserAdmin):
    model = User
    list_editable = (
        'username',
        'first_name',
        'last_name',
        'email',
        'is_staff',
        'is_active',
        'role'
    )
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
        'is_staff',
        'is_active',
        'role'
    )
    ordering = ('username',)
    search_fields = ('username', 'email',)
    ordering = ('username',)


admin.site.register(Follow)
