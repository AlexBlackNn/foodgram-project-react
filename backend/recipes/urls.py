from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    DownloadShoppingCart,
    FavoriteView,
    RecipeViewSet,
    ShoppingView,
    IngredientViewSet,
    TagView
)

router = DefaultRouter()
router.register('tags', TagView, basename='tags')
router.register('recipes', RecipeViewSet)
router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('recipes/download_shopping_cart/', DownloadShoppingCart.as_view()),
    path('', include(router.urls)),
    path('recipes/<int:recipe_id>/favorite/', FavoriteView.as_view()),
    path('recipes/<int:recipe_id>/shopping_cart/', ShoppingView.as_view()),
]

