# views.py
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.hashers import make_password, check_password

from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import AccessToken

from .models import User, Tag
from .serializers import TagSerializer, UserSerializer, TokenSerializer


class APISignUp(generics.ListCreateAPIView):
    """Регистрация пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    # регестрация доступна всем
    permission_classes = (AllowAny,)
    def post(self, request):
        """Пользователь отправил email и usernameна эндпоинт .../signup/."""
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(role='user')
        # Берем пользователя, который только, что был создан
        username = serializer.data['username']
        user = get_object_or_404(User, username=username)

        return Response(
            {'email': serializer.data['email'],
             'username': serializer.data['username'],
             'first_name': serializer.data['first_name'],
             'last_name': serializer.data['last_name']},
            status=status.HTTP_200_OK
        )


class APIToken(generics.CreateAPIView):
    """Регистрация пользователя."""

    # регестрация доступна всем
    permission_classes = (AllowAny,)

    def post(self, request):
        """Пользователь отправил email и password на  эндпоинт .../login/."""
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Берем пользователя, который только, что был создан
        email = serializer.data['email']
        user = get_object_or_404(User, email=email)
        if check_password(serializer.data['password'], user.password):
            token = AccessToken.for_user(user)
            return Response(
                {'auth_token': str(token)},
                status=status.HTTP_200_OK
            )
        return Response(
            {'auth_token': 'Wrong password!'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class APIUser(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (IsAdmin,)
    permission_classes = (AllowAny,)
    lookup_field = 'username'
    search_fields = ('username',)

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


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer