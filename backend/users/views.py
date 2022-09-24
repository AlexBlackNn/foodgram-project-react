from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Follow, User
from .serializers import (FollowSubscriptionSerializer, PasswordSerializer,
                          UserFollowSerializer, UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny, ]

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[IsAuthenticated],
        url_path='set_password'
    )
    def set_password(self, request, *args, **kwargs):
        user = request.user
        serializer = PasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.data['new_password']
        current_password = serializer.data['current_password']
        if check_password(current_password, user.password):
            user.set_password(new_password)
            user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {'auth_token': 'Wrong password!'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class FollowSubscribeApiView(APIView):
    """users/<int:following_id>/subscribe/"""

    permission_classes = [IsAuthenticated, ]

    def post(self, request, following_id):
        serializer = UserFollowSerializer(
            data={'author': following_id, 'user': request.user.id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, following_id):
        author = get_object_or_404(User, id=following_id)
        Follow.objects.filter(user=request.user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowSubscriptionApiView(generics.ListAPIView):
    """users/subscriptions/"""

    permission_classes = [IsAuthenticated, ]
    serializer_class = FollowSubscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(following__user=user)
