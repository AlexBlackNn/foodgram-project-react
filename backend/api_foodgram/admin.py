from django.contrib import admin

from .models import (
    User,
    Tag,
    Ingredients,
    Recipe,
    RecipeIngredients,
    Follow
)

admin.site.register(User)


class TagAdmin(admin.ModelAdmin):
    """Настройка админки."""

    list_display = ('pk', 'name', 'color', 'slug', 'recipe',)
    list_editable = ('name', 'color', 'slug')
    search_fields = ('name','slug')
    list_filter = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Tag, TagAdmin)

class RecipeAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'author',
        'name',
        'image',
        'text',
        'cooking_time',
        'is_favorited',
        'is_in_shopping_cart',
        'pub_date'
    )
    list_filter = ('pub_date',)

class IngredientsAdmin(admin.ModelAdmin):
    """Настройка админки."""

    list_display = ('pk', 'measurement_unit')

admin.site.register(Ingredients, IngredientsAdmin)



class FollowAdmin(admin.ModelAdmin):
    """Настройка админки."""

    list_display = ('user', 'author',)
    list_editable = ('author',)

admin.site.register(Follow, FollowAdmin)