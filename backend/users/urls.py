from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import APICreateToken, APIDestroyToken, UserViewSet

router = DefaultRouter()

router.register('users', UserViewSet, basename='users')

urls_token = [
    path('login/', APICreateToken.as_view(), name='create_token'),
    path('logout/', APIDestroyToken.as_view(), name='create_token')
]

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', include(urls_token)),
    # path('users/(?P<id>\d+)/subscribe/'))
]

#
# router.register(
#     r'users/(?P<id>\d+)/subscribe/',
#     FollowViewSet,
#     basename='follow'
# )