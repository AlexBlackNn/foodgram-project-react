from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import (
    SAFE_METHODS,
    AllowAny,
    IsAuthenticated,
)

from api.filters import RecipeFilterSet, IngredientFilterSet
from api.pagination import LimitPaginator
from api.serializers import (
    TagSerializer,
    RecipeReadSerializer,
    RecipeWriteSerializer, FavoriteSerializer, BaseIngredientSerializer,
    CartSerializer,
)
from api.permissions import (
    IsAuthorOrAdministratorOrReadOnly,
    IsAdminOrReadOnly
)

from recipes.models import (
    Recipe,
    Tag,
    Ingredient,
    Favorite,
    ShoppingCart,
    IngredientQuantity
)

CONTENT_TYPE = 'text/plain'
FILENAME = 'shopping_list.txt'


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    pagination_class = LimitPaginator
    permission_classes = (IsAuthorOrAdministratorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilterSet
    queryset = Recipe.objects.all()
    http_method_names = ['get', 'post', 'head', 'put', 'patch', 'delete']
    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer = RecipeReadSerializer(instance=serializer.instance)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        serializer = RecipeReadSerializer(instance=serializer.instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_200_OK,
                        headers=headers)


class FavoriteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()
    model = Favorite

    def create(self, request, *args, **kwargs):
        recipe_id = int(self.kwargs['recipes_id'])
        recipe = get_object_or_404(Recipe, id=recipe_id)
        self.model.objects.create(
            user=request.user, recipe=recipe)
        serializer = FavoriteSerializer()
        return Response(serializer.to_representation(instance=recipe),
                        status=status.HTTP_201_CREATED
                        )

    def delete(self, request, *args, **kwargs):
        recipe_id = self.kwargs['recipes_id']
        user_id = request.user.id
        object = get_object_or_404(
            self.model, user__id=user_id, recipe__id=recipe_id)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = BaseIngredientSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = IngredientFilterSet
    search_fields = ('^name',)


class ShoppingCartViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CartSerializer
    pagination_class = LimitPaginator
    queryset = ShoppingCart.objects.all()
    model = ShoppingCart

    def create(self, request, *args, **kwargs):
        recipe_id = int(self.kwargs['recipes_id'])
        recipe = get_object_or_404(Recipe, id=recipe_id)
        self.model.objects.create(
            user=request.user, recipe=recipe)
        serializer = CartSerializer()
        return Response(serializer.to_representation(instance=recipe),
                        status=status.HTTP_201_CREATED
                        )

    def delete(self, request, *args, **kwargs):
        recipe_id = self.kwargs['recipes_id']
        user_id = request.user.id
        object = get_object_or_404(
            self.model, user__id=user_id, recipe__id=recipe_id)
        print('--------------->>>>', object)
        object.delete()
        return Response(status.HTTP_204_NO_CONTENT)

    def download(self, request):
        shopping_list = IngredientQuantity.objects.filter(
            recipe__shopping_cart__user=request.user).values(
            'ingredient__name', 'ingredient__measurement_unit').order_by(
            'ingredient__name').annotate(ingredient_total=Sum('amount'))

        content = (
            [
                f'{item["ingredient__name"]} ({item["ingredient__measurement_unit"]})'
                f'- {item["ingredient_total"]}\n'
                for item in shopping_list]
        )
        response = HttpResponse(content, content_type=CONTENT_TYPE)
        response['Content-Disposition'] = (
            f'attachment; filename={FILENAME}'
        )
        return response
