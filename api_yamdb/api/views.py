from django.apps import apps
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings as cfg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, pagination, filters
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, CreateModelMixin, \
    DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews import models

from . import serializers
from .filters import TitleFilter
from .mixins import CreateMixin
from .permissions import AdminOrReadOnly

User = apps.get_model(app_label='reviews', model_name='User')


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (AdminOrReadOnly,)
    pagination_class = pagination.PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    queryset = User.objects.all()

    def get_serializer_class(self):
        if (
            self.request.user.is_authenticated and (
                self.request.user.is_superuser or
                self.request.user.is_staff or
                self.request.user.permission_level() == 2
            )
        ):
            return serializers.UserSerializer
        return serializers.UserCreationSerializer

    def retrieve(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=kwargs.get('pk'))
        return Response(self.serializer_class(user).data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = get_object_or_404(
            self.get_queryset(),
            username=kwargs.get('pk')
        )
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not (
            self.request.user.is_authenticated and (
                self.request.user.is_superuser or
                self.request.user.is_staff or
                self.request.user.permission_level() == 2
            )
        ):
            user = User.objects.create(request.data)
            send_mail(
                subject='YAMDB auth',
                message=str(AccessToken.for_user(user)),
                recipient_list=[user.email],
                from_email=cfg.DEFAULT_FROM_EMAIL,
            )
            return Response(self.get_serializer(user))
        else:
            user = User.objects.create(request.data)
            return Response(self.get_serializer(user))

    @action(
        url_path='me',
        detail=True,
        methods=['GET', 'PATCH'],
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        serializer = self.get_serializer(request.user, many=False)
        return Response(serializer.data)


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
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.TitleReadOnlySerializer
        return serializers.TitleEditSerializer

