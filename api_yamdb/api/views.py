from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin,
    ListModelMixin
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from . import permissions
from . import serializers
from .filters import TitleFilter
from api_yamdb.settings import CODE_LENGTH
from reviews.models import Category, Title, Genre, Review, User


EMAIL_SUBJECT = 'Код подтверждения для проекта YamDB'
EMAIL_MESSAGE = '{}, Ваш код подтверждения: {}'


def set_code(user):
    user.confirmation_code = get_random_string(
        CODE_LENGTH, '123456789')
    user.save()
    return user.confirmation_code


def send_code(user):
    """
    Аргумент 'from_email' содержит адрес отправителя.
    Если не определён или 'None' в качестве адреса
    отправителя используется заданное по умолчанию
    в DEFAULT_FROM_EMAIL 'webmaster@localhost'.
    """
    send_mail(
        subject=EMAIL_SUBJECT,
        message=EMAIL_MESSAGE.format(
            user.username,
            user.confirmation_code
        ),
        from_email=None,
        recipient_list=[user.email]
    )


class APIToken(APIView):

    def post(self, request):
        serializer = serializers.UsernameCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=serializer.data['username'])
        if serializer.data['confirmation_code'] == str(
            user.confirmation_code
        ) and user.is_active:
            token = {'token': str(AccessToken.for_user(user))}
            return Response(token, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class APISignUp(APIView):

    def post(self, request):
        serializer = serializers.SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, created = User.objects.get_or_create(
                username=serializer.data['username'],
                email=serializer.data['email']
            )
        except IntegrityError:
            raise ValidationError('Указанные username или email уже заняты.')
        set_code(user)
        send_code(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class APIMeUser(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request):
        return Response(serializers.MeSerializer(request.user).data)

    def patch(self, request):
        serializer = serializers.MeSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializers.MeSerializer(request.user).data,
            status=status.HTTP_200_OK
        )


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAdmin,)
    search_fields = 'username'
    lookup_field = 'username'


class CategoryGenreViewSet(GenericViewSet, CreateModelMixin,
                           DestroyModelMixin, ListModelMixin):
    permission_classes = (permissions.IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class CategoriesViewSet(CategoryGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategoriesSerializer


class GenresViewSet(CategoryGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenresSerializer


class TitlesViewSet(ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    permission_classes = (permissions.IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('rating',)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return serializers.TitlesReadOnlySerializer
        return serializers.TitlesSerializer


class ReviewsViewSet(ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_classes = (permissions.IsAuthorAdminModeratorOrReadOnly,)

    def get_title_or_404(self):
        return get_object_or_404(
            Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title_or_404().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title_or_404()
        )


class CommentsViewSet(ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthorAdminModeratorOrReadOnly,)

    def get_rewiew_or_404(self):
        return get_object_or_404(
            Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_rewiew_or_404().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_rewiew_or_404()
        )
