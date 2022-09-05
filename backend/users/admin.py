from django.contrib import admin
from .models import Follow, User
# Register your models here.

class FollowAdmin(admin.ModelAdmin):
    """Настройка админки."""

    list_display = ('user', 'author',)
    list_editable = ('author',)


admin.site.register(Follow, FollowAdmin)
admin.site.register(User)