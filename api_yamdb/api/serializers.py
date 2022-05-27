from django.contrib.auth.validators import ASCIIUsernameValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import IntegerField

from api_yamdb.settings import CODE_LENGTH, EMAIL_LENGTH, USERNAME_LENGTH
from reviews import models
from reviews.validators import (
    check_year_validation, check_score,
    not_me_username_validation)


class UsernameSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=USERNAME_LENGTH,
        validators=[ASCIIUsernameValidator(),
                    not_me_username_validation])


class UsernameCodeSerializer(UsernameSerializer):
    confirmation_code = serializers.CharField(
        max_length=CODE_LENGTH)


class SignUpSerializer(UsernameSerializer):
    email = serializers.EmailField(
        max_length=EMAIL_LENGTH)


class UserSerializer(serializers.ModelSerializer,
                     UsernameSerializer):

    def validate_username(self, value):
        if models.User.objects.filter(username=value).exists():
            raise ValidationError(
                f'Имя пользователя {value} уже существует.')
        return value

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = models.User


class MeSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Genre
        fields = ('name', 'slug')


class TitlesReadOnlySerializer(serializers.ModelSerializer):
    category = CategoriesSerializer()
    genre = GenresSerializer(many=True)
    rating = serializers.IntegerField()

    class Meta:
        model = models.Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        read_only_fields = ('__all__',)


class TitlesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=models.Category.objects.all(),
        slug_field='slug')
    genre = serializers.SlugRelatedField(
        queryset=models.Genre.objects.all(),
        slug_field='slug', many=True)
    year = IntegerField(validators=[check_year_validation])

    class Meta:
        model = models.Title
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)
    score = IntegerField(validators=[check_score])

    def validate(self, attrs):
        title = get_object_or_404(
            models.Title,
            id=self.context.get('view').kwargs.get('title_id'))
        request = self.context.get('request')
        if (request.method != 'PATCH'
            and models.Review.objects.filter(
                title_id=title.id, author=request.user).exists()):
            raise serializers.ValidationError(
                'Вы уже писали отзыв на это произведение')
        return attrs

    class Meta:
        model = models.Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = models.Comment
        fields = ('id', 'text', 'author', 'pub_date')
