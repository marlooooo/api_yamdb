from django.apps import apps
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews import models


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
                'Имя пользователя не может быть "me".'
            )
        return value


class UserSerializer(UserCreationSerializer):
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


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)


class TokenObtainSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанра"""
    class Meta:
        model = models.Genre
        exclude = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категории"""
    class Meta:
        model = models.Category
        exclude = ('id',)


class TitleReadOnlySerializer(serializers.ModelSerializer):
    """Сериализатор для тайтлов на чтение"""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.FloatField()

    class Meta:
        fields = ('id', 'name', 'year', 'description',
                  'category', 'genre', 'rating')
        read_only_fields = ('id', 'rating')
        model = models.Title


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

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'category',
                  'genre')
        model = models.Title


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

    def validate(self, data):
        """Проверка, что от одного человека на конкретное произведение
        только один отзыв."""
        request = self.context.get('request')
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(models.Title, id=title_id)
        if request.method != 'PATCH' and (models.Review.objects
                                          .filter(author=author, title=title)
                                          .exists()):
            raise serializers.ValidationError(
                'Только один отзыв на произведение'
            )
        return data


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
