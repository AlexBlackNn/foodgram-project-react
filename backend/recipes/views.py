from django.shortcuts import HttpResponse, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import RecipeFilter
from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     ShoppingList, Tag)
from .permissions import IsAuthorOrAdministratorOrReadOnly
from .serializers import (FavoriteShoppingReturnSerializer,
                          FavoriteWriteSerializer, IngredientSerializer,
                          RecipeFullSerializer, RecipeSafeSerializer,
                          ShoppingListWriteSerializer, TagSerializer)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Получить ингредиенты."""

    serializer_class = IngredientSerializer
    permission_classes = [AllowAny, ]
    queryset = Ingredient.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # Поиск по частичному вхождению в начале названия ингредиента.
    search_fields = ('^name',)
    pagination_class = None


class TagView(viewsets.ReadOnlyModelViewSet):
    """Получить теги."""

    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Работа с рецептами."""

    permission_classes = [IsAuthorOrAdministratorOrReadOnly, ]
    queryset = Recipe.objects.all()

    filter_backends = [DjangoFilterBackend, ]
    filterset_class = RecipeFilter

    pagination_class = PageNumberPagination
    pagination_class.page_size = 6

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeSafeSerializer
        return RecipeFullSerializer

    @action(
        detail=False,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
        url_path=r'(?P<recipe_id>[0-9]+)/favorite',
    )
    def favorite(self, request, recipe_id):
        if request.method == 'POST':
            recipe = get_object_or_404(Recipe, id=recipe_id)
            serializer = FavoriteWriteSerializer(
                data={'recipe': recipe_id, 'user': request.user.id},
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            serializer = FavoriteShoppingReturnSerializer()
            return Response(
                serializer.to_representation(instance=recipe),
                status=status.HTTP_201_CREATED
            )
        else:
            user = request.user
            favorite = get_object_or_404(
                Favorite, user=user, recipe__id=recipe_id
            )
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
        url_path=r'(?P<recipe_id>[0-9]+)/shopping_cart',
    )
    def shopping(self, request, recipe_id):
        if request.method == 'POST':
            recipe = get_object_or_404(Recipe, id=recipe_id)
            serializer = ShoppingListWriteSerializer(
                data={'recipe': recipe_id, 'user': request.user.id},
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            serializer = FavoriteShoppingReturnSerializer()
            return Response(
                serializer.to_representation(instance=recipe),
                status=status.HTTP_201_CREATED
            )
        else:
            user = request.user
            recipe = get_object_or_404(Recipe, id=recipe_id)
            ShoppingList.objects.filter(user=user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class DownloadShoppingCart(APIView):
    """Скачивание файла с продуктами для рецептов."""

    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        shopping_list = {}
        ingredients = IngredientAmount.objects.filter(
            recipe__purchases__user=request.user
        )
        for ingredient in ingredients:
            amount = ingredient.amount
            name = ingredient.ingredient.name
            measurement_unit = ingredient.ingredient.measurement_unit

            shopping_list.setdefault(name, {
                'measurement_unit': measurement_unit,
                'amount': amount
            })

            shopping_list[name]['amount'] += amount

        resulted_list = []
        for num, data in enumerate(shopping_list.items(), 1):
            item = data[0]
            value = data[1]
            resulted_list.append(f"{num}) {item}:{value['amount']}"
                                 f"{value['measurement_unit']}\n")

        return HttpResponse(
            resulted_list,
            'Content-Type: text/plain'
        )
