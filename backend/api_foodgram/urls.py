from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import APISignUp, APIToken, TagViewSet

router = DefaultRouter()

router.register('tags', TagViewSet, basename='tags')

urls_auth = [
    # Пользователь отправляет POST-запрос на добавление нового пользователя
    # с параметрами email и password в ответ токен
    path('users/', APISignUp.as_view(), name='signup'),
    path('auth/login/', APIToken.as_view(), name='signup'),

]

urlpatterns = [
    path('', include(router.urls)),
    path('', include(urls_auth))
]
