from django.urls import include, path
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.routers import DefaultRouter

from .views import TagViewSet, RecipeViewSet, FavoriteViewSet, ShoppingCartViewSet

router = DefaultRouter()

router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')

@api_view()
def hello_world(request):
    return Response({"message": "Hello, world!"})

urlpatterns = [
    path('recipes/<recipes_id>/favorite/',
         FavoriteViewSet.as_view({'post': 'create',
                                  'delete': 'delete'}), name='favorite'),
    path('recipes/create:8000/', hello_world),
    path('', include(router.urls)),
    path('recipes/download_shopping_cart/',
         ShoppingCartViewSet.as_view({'get': 'download'}), name='download'),
    path('recipes/<recipes_id>/shopping_cart/',
         ShoppingCartViewSet.as_view({'post': 'create',
                              'delete': 'delete'}), name='cart'),
]