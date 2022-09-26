from django.contrib import admin
from django.db.models import Sum

from .models import (
    Favorite,
    Ingredient,
    IngredientAmount,
    Recipe,
    ShoppingList,
    Tag
)

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
        'get_quantity_the_recipy_is_favorite',
        'get_ingredients',
    )
    search_fields = ('author', 'name')
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-пусто-'

    def get_quantity_the_recipy_is_favorite(self, obj):
        return obj.favorites.count()

    get_quantity_the_recipy_is_favorite.short_description = (
        'Количество пользователей, добавившее рецепт в избранное'
    )

    def get_ingredients(self, obj):
        queury_set = (obj.recipes_ingredients_list.all().values(
            'ingredient__name',
            'ingredient__measurement_unit',
        ).annotate(
            ingredient_amount=Sum('amount')
        ))
        ingredient_description = ''
        for item in queury_set:
            ingredient_row = (
                f'{item["ingredient__name"]}'
                f' {item["ingredient_amount"]}'
                f' {item["ingredient__measurement_unit"]}'
                '\n'
            )
            ingredient_description += ingredient_row
        return ingredient_description

    get_ingredients.short_description = (
        'Ингредиенты'
    )
