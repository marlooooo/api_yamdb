from abc import ABC

from django.apps import apps
from django.db.models import Avg
# from django.conf import settings

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews import models

# Доступ к моделям через apps.get_model(app_label='review', model_name='User')


User = apps.get_model(app_label='reviews', model_name='User')


class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=(
                    'username',
                    'email',
                ),
            ),
        ]

    def validate_username(self, value):
        """Проверяет правильность содержания поля username."""
        if 'me' == value.lower():
            raise serializers.ValidationError(
                f'Имя пользователя не может быть "{value.lower()}".'
            )
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=(
                    'username',
                    'email',
                ),
            ),
        ]

    def validate_username(self, value):
        if 'me' == value.lower():
            raise serializers.ValidationError(
                'Имя пользователя не может быть me.'
            )
        return value


class NotAdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        read_only_fields = ('role',)
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=(
                    'username',
                    'email',
                ),
            ),
        ]

    def validate_username(self, value):
        if 'me' == value.lower():
            raise serializers.ValidationError(
                'Имя пользователя не может быть me.'
            )
        return value


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)


class TokenObtainSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    conformation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'conformation_code')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанра"""
    class Meta:
        fields = ('name', 'slug')
        model = models.Genre


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категории"""
    class Meta:
        fields = ('name', 'slug')
        model = models.Category


class TitleReadOnlySerializer(serializers.ModelSerializer):
    """Сериализатор для тайтлов на чтение"""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'year', 'description',
                  'category', 'genre', 'rating')
        model = models.Title

    def get_rating(self, obj):
        avg_score = (
            models.Review.objects.filter(title__id=obj.id)
            .aggregate(Avg('score')).get('score__avg')
        )
        return avg_score


class TitleEditSerializer(serializers.ModelSerializer):
    """Сериализатор для тайтлов на запись"""
    category = serializers.SlugRelatedField(
        queryset=models.Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=models.Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'category',
                  'genre', 'rating')
        model = models.Title

    def get_rating(self, obj):
        avg_score = (
            models.Review.objects.filter(title__id=obj.id)
            .aggregate(Avg('score')).get('score__avg')
        )
        return avg_score


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    pub_date = serializers.DateTimeField(read_only=True)

    class Meta:
        fields = ('id', 'text', 'score', 'author', 'pub_date')
        model = models.Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    pub_date = serializers.DateTimeField(read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = models.Comment
