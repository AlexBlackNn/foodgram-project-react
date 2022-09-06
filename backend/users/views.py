from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets

from .models import User
from .serializers import (
    UserSerializer,
    PasswordSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
        url_path='me'
    )
    def me(self, request, *args, **kwargs):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[IsAuthenticated],
        url_path='set_password'
    )
    def set_password(self, request, *args, **kwargs):
        user = request.user
        if request.method == 'POST':
            serializer = PasswordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            # Берем пользователя, который только, что был создан
            new_password = serializer.data['new_password']
            current_password = serializer.data['current_password']
            if check_password(current_password, user.password):
                user.set_password(new_password)
                user.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            return Response(
                {'auth_token': 'Wrong password!'},
                status=status.HTTP_401_UNAUTHORIZED
            )
