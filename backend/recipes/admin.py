from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     ShoppingList, Tag)

admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(IngredientAmount)
admin.site.register(ShoppingList)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit'
    )
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class IngredientsInline(admin.TabularInline):
    model = Ingredient

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'name',
        'image',
        'text',
        'is_favorited',
        'ingredients',
    )
    search_fields = ('author', 'name')
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-пусто-'

    def is_favorited(self, obj):
        return obj.favorites.count()

    def ingredients(self, obj):
        return list(obj.ingredients.all())

    ingredients.short_description = 'Ингредиенты'

