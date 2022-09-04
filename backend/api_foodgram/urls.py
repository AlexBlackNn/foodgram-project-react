from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import APIToken, APIUser, TagViewSet

router = DefaultRouter()

router.register('users', APIUser, basename='users')
router.register('tags', TagViewSet, basename='tags')

urls_auth = [
    # Пользователь отправляет POST-запрос на добавление нового пользователя
    # с параметрами email и password в ответ токен
    path('auth/token/login/', APIToken.as_view(), name='token'),

]

urlpatterns = [
    path('', include(router.urls)),
    path('', include(urls_auth))
]
