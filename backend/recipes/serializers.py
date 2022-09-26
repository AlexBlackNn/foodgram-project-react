from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import User
from users.serializers import UserSerializer

from .fields import Base64ImageField
from .models import (
    Favorite,
    Ingredient,
    IngredientAmount,
    Recipe,
    ShoppingList,
    Tag
)


class TagSerializer(serializers.ModelSerializer):
    """Работам с тэгами"""

    class Meta:
        model = Tag
        fields = ('__all__')
        lookup_field = 'id'
        extra_kwargs = {'url': {'lookup_field': 'id'}}


class IngredientSerializer(serializers.ModelSerializer):
    """Получение ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ('__all__')


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        read_only=True
    )
    name = serializers.SlugRelatedField(
        slug_field='name',
        source='ingredient',
        read_only=True
    )
    measurement_unit = serializers.SlugRelatedField(
        slug_field='measurement_unit',
        source='ingredient',
        read_only=True
    )

    class Meta:
        model = IngredientAmount
        fields = '__all__'


class AddToIngredientAmountSerializer(serializers.ModelSerializer):
    """Serializer для ингредиентов RecipeFullSerializer"""

    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientAmount
        fields = ('amount', 'id')


class RecipeSafeSerializer(serializers.ModelSerializer):
    """Для методов SAFE_METHODS"""

    author = UserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)

    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited'
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart'
    )
    ingredients = serializers.SerializerMethodField(
        method_name='get_ingredients'
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, recipe):
        user = self.context['request'].user
        return (
            user.is_authenticated
            and Favorite.objects.filter(recipe=recipe, user=user).exists()
        )

    def get_is_in_shopping_cart(self, recipe):
        user = self.context['request'].user
        return (
            user.is_authenticated
            and ShoppingList.objects.filter(recipe=recipe, user=user).exists()
        )

    def get_ingredients(self, recipe):
        queryset = recipe.recipes_ingredients_list.all()
        return IngredientAmountSerializer(queryset, many=True).data


class RecipeFullSerializer(serializers.ModelSerializer):
    """Для методов отличных от SAFE_METHODS"""

    image = Base64ImageField()
    author = UserSerializer(read_only=True)
    ingredients = AddToIngredientAmountSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'image',
            'tags',
            'author',
            'ingredients',
            'name',
            'text',
            'cooking_time'
        )

    @staticmethod
    def __ingredient_amount_bulk_create(recipe, ingredients_data):
        IngredientAmount.objects.bulk_create([IngredientAmount(
            ingredient=ingredient['ingredient'],
            recipe=recipe,
            amount=ingredient['amount']
        ) for ingredient in ingredients_data])

    def create(self, validated_data):
        # Делаем селекцию данных
        user = self.context['request'].user
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        # Создаем объект рецепта
        recipe = Recipe.objects.create(author=user, **validated_data)
        recipe.save()
        # Добавляем к нему теги
        recipe.tags.set(tags_data)
        # создаем объекты IngredientAmount
        self.__ingredient_amount_bulk_create(recipe, ingredients_data)
        return recipe

    def update(self, recipe, validated_data):
        # Делаем селекцию данных
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')

        # Удаляем старые объекты
        IngredientAmount.objects.filter(recipe=recipe).delete()
        # Создаем новые объекты
        self.__ingredient_amount_bulk_create(recipe, ingredients_data)

        recipe.name = validated_data.pop('name')
        recipe.text = validated_data.pop('text')
        recipe.cooking_time = validated_data.pop('cooking_time')

        if validated_data.get('image'):
            recipe.image = validated_data.pop('image')

        recipe.save()
        recipe.tags.set(tags_data)
        return recipe

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        for ingredient in ingredients:
            if int(ingredient['amount']) <= 0:
                raise serializers.ValidationError({
                    f'ingredients': (
                        'Убедитесь, что это значение больше 0.'
                    )
                })
        return data

    def to_representation(self, instance):
        return RecipeSafeSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data


class FavoriteShoppingWriteSerializer(serializers.ModelSerializer):
    """Родительский класс для добавления в список покупок и избранное."""

    recipe = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Recipe.objects.all(),
    )
    user = serializers.SlugRelatedField(
        slug_field='id',
        queryset=User.objects.all(),
    )

    class Meta:
        model = ShoppingList
        fields = ('user', 'recipe')


class ShoppingListWriteSerializer(FavoriteShoppingWriteSerializer):
    """Запись в список покупок."""

    class Meta:
        model = ShoppingList
        fields = FavoriteShoppingWriteSerializer.Meta.fields
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingList.objects.all(),
                fields=['user', 'recipe'],
                message="Уже добавлен!"
            )
        ]


class FavoriteWriteSerializer(FavoriteShoppingWriteSerializer):
    """Запись рецептов в избранное."""

    class Meta:
        model = Favorite
        fields = FavoriteShoppingWriteSerializer.Meta.fields
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['user', 'recipe'],
                message="Уже добавлен!"
            )
        ]


class FavoriteShoppingReturnSerializer(serializers.ModelSerializer):
    """Для ответа при дабовление в избранное."""

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
