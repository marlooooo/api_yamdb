from django.apps import apps
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, pagination, filters
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin


from reviews import models
from . import serializers
from .permissions import AdminOrReadOnly

User = apps.get_model(app_label='reviews', model_name='User')


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (
        AdminOrReadOnly,
    )
    pagination_class = pagination.LimitOffsetPagination
    serializer_class = serializers.UserAdminSerializer
    filter_backends = (
        filters.SearchFilter,
    )
    search_fields = (
        'username',
        'email',
    )
    queryset = User.objects.all()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = models.Title.objects.all()
    serializer_class = serializers.TitleSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSeiralizer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(models.Title, id=self.kwargs.get('title_id'))
        queryset = models.Review.objects.filter(title=title)
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=models.Title.objects.get(id=self.kwargs.get('title_id'))
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(models.Review,
                                   id=self.kwargs.get('review_id'))
        queryset = models.Comment.objects.filter(review=review)
        return queryset


class GenreViewSet(viewsets.GenericViewSet, ListModelMixin, CreateModelMixin, DestroyModelMixin):
    """Вьюсет для жанров"""
    permission_classes = (AdminOrReadOnly,)
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)


class CategoryViewSet(viewsets.GenericViewSet, ListModelMixin, CreateModelMixin, DestroyModelMixin):
    """Вьюсет для категорий"""
    permission_classes = (AdminOrReadOnly,)
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для тайтлов"""
    permission_classes = (AdminOrReadOnly,)
    queryset = models.Title.objects.all()

