from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import APICreateToken,APIDestroyToken, UserViewSet, TagViewSet

router = DefaultRouter()

router.register('users', UserViewSet, basename='users')
router.register('tags', TagViewSet, basename='tags')

urls_auth = [
    # Пользователь отправляет POST-запрос на добавление нового пользователя
    # с параметрами email и password в ответ токен
    path('auth/token/login/', APICreateToken.as_view(), name='create_token'),
    path('auth/token/logout/', APIDestroyToken.as_view(), name='create_token')
]

urlpatterns = [
    path('', include(router.urls)),
    path('', include(urls_auth))
]
