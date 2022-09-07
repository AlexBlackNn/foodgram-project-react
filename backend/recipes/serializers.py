import base64

from rest_framework.fields import SerializerMethodField, ListField
from rest_framework.serializers import ModelSerializer, ImageField
from .models import Tag, Recipe, ShoppingCart
from django.core.files.base import ContentFile
from ..users.serializers import UserSerializer


class TagSerializer(ModelSerializer):
    """Сериализатор для tags."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class Base64ImageField(ImageField):

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)

class RecipeSerializer(ModelSerializer):

    image = Base64ImageField(required=False, allow_null=True)
    author = UserSerializer(read_only=True, many=False)
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Recipe
        fields = (
            'author',
            'tags',
            'name',
            'image',
            'text',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart',
            'pub_date',
        )


class RecipeReadSerializer(ModelSerializer):
    tags = TagSerializer(many=True)
    author = UserSerializer()
    ingredients = RecipeIngredientReadSerializer(many=True)
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'image', 'text', 'cooking_time',
        )

    def get_user(self):
        return self.context['request'].user

    def get_is_favorited(self, obj):
        user = self.get_user()
        return (
            user.is_authenticated
            and user.favorites.filter(recipe=obj).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        user = self.get_user()
        try:
            return (
                user.is_authenticated and
                user.shopping_cart.recipes.filter(pk__in=(obj.pk,)).exists()
            )
        except ShoppingCart.DoesNotExist:
            return False


class RecipeWriteSerializer(ModelSerializer):
    ingredients = RecipeIngredientWriteSerializer(many=True)
    tags = ListField(
        child=SlugRelatedField(
            slug_field='id',
            queryset=Tag.objects.all(),
        ),
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time',
        )
        extra_kwargs = {
            'cooking_time': {
                'error_messages': {
                    'min_value': COOKING_TIME_MIN_ERROR,
                }
            }
        }

    def validate(self, attrs):
        if attrs['cooking_time'] < COOKING_TIME_MIN_VALUE:
            raise ValidationError(COOKING_TIME_MIN_ERROR)
        if len(attrs['tags']) == 0:
            raise ValidationError(TAGS_EMPTY_ERROR)
        if len(attrs['tags']) > len(set(attrs['tags'])):
            raise ValidationError(TAGS_UNIQUE_ERROR)
        if len(attrs['ingredients']) == 0:
            raise ValidationError(INGREDIENTS_EMPTY_ERROR)
        id_ingredients = []
        for ingredient in attrs['ingredients']:
            if ingredient['amount'] < INGREDIENT_MIN_AMOUNT:
                raise ValidationError(
                    INGREDIENT_MIN_AMOUNT_ERROR.format(
                        min_value=INGREDIENT_MIN_AMOUNT,
                    )
                )
            id_ingredients.append(ingredient['id'])
        if len(id_ingredients) > len(set(id_ingredients)):
            raise ValidationError(INGREDIENTS_UNIQUE_ERROR)
        return attrs

    def add_ingredients_and_tags(self, instance, validated_data):
        ingredients, tags = (
            validated_data.pop('ingredients'), validated_data.pop('tags')
        )
        for ingredient in ingredients:
            count_of_ingredient, _ = CountOfIngredient.objects.get_or_create(
                ingredient=get_object_or_404(Ingredient, pk=ingredient['id']),
                amount=ingredient['amount'],
            )
            instance.ingredients.add(count_of_ingredient)
        for tag in tags:
            instance.tags.add(tag)
        return instance

    def create(self, validated_data):
        saved = {}
        saved['ingredients'] = validated_data.pop('ingredients')
        saved['tags'] = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        return self.add_ingredients_and_tags(recipe, saved)

    def update(self, instance, validated_data):
        instance.ingredients.clear()
        instance.tags.clear()
        instance = self.add_ingredients_and_tags(instance, validated_data)
        return super().update(instance, validated_data)