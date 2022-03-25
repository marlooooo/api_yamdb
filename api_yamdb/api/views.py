from django.apps import apps
from django.conf import settings as cfg
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, pagination, filters, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from reviews import models
from . import serializers
from .filters import TitleFilter
from .mixins import CreateMixin, CategoriesGenresMixin
from .permissions import (
    AdminOrReadOnly, OwnerOrReadOnly, UserViewSetPermission
)

User = apps.get_model(app_label='reviews', model_name='User')


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (UserViewSetPermission,)
    pagination_class = pagination.PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'username'

    @action(
        url_path='me',
        detail=False,
        methods=('GET', 'PATCH'),
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        serializer = serializers.UserSerializer(request.user)
        if request.method == 'GET':
            return Response(serializer.data, status=status.HTTP_200_OK)
        data = request.data
        if not (request.user.is_admin or request.user.is_superuser):
            if 'role' in data:
                data._mutable = True
                data['role'] = request.user.role
                data._mutable = False
        serializer = serializers.UserSerializer(
            request.user, data=data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserCreationViewSet(CreateMixin):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserCreationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = self.get_queryset().get(
            username=serializer.validated_data.get('username'),
            email=serializer.validated_data.get('email')
        )
        token = Token.objects.get_or_create(user_id=user.id)[0]
        key = token.key
        send_mail(
            subject='ACCESS TOKEN',
            message=f'{user.username.capitalize()}, you\''
                    f'r key is\n key - "{key}"',
            from_email=cfg.DEFAULT_FROM_EMAIL,
            recipient_list=(user.email,)
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomTokenObtainView(APIView):
    def post(self, request):
        serializer = serializers.TokenObtainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            _user = User.objects.get(
                username=serializer.validated_data.get('username'))
        except User.DoesNotExist:
            return Response(
                {'username': 'Проверьте правильность username'},
                status=status.HTTP_404_NOT_FOUND,
            )
        if Token.objects.filter(
            user_id__exact=_user.id,
            key__exact=serializer.validated_data.get('confirmation_code')
        ).exists():
            return Response(
                {'token': str(AccessToken.for_user(_user))},
                status=status.HTTP_200_OK
            )
        return Response(
            {'token': 'Проверьте правильность кода подтверждения'},
            status=status.HTTP_400_BAD_REQUEST
        )


class GenreViewSet(CategoriesGenresMixin):
    """Вьюсет для жанров"""
    permission_classes = (AdminOrReadOnly,)
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)


class CategoryViewSet(CategoriesGenresMixin):
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
    queryset = models.Title.objects.all().annotate(rating=Avg('reviews__score'))
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.TitleReadOnlySerializer
        return serializers.TitleEditSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для ревью"""
    permission_classes = (OwnerOrReadOnly,)
    serializer_class = serializers.ReviewSerializer
    lookup_field = 'id'

    def get_queryset(self):
        title = get_object_or_404(models.Title, id=self.kwargs.get('title_id'))
        queryset = models.Review.objects.filter(title=title)
        return queryset

    def perform_create(self, serializer):
        author = self.request.user
        title = get_object_or_404(models.Title, id=self.kwargs.get('title_id'))
        if models.Review.objects.filter(author=author, title=title).exists():
            raise ValidationError('Только один отзыв на произведение')
        else:
            serializer.save(
                author=author,
                title=title
            )


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (OwnerOrReadOnly,)
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(
            models.Review,
            id=self.kwargs.get('review_id'),
        )
        queryset = models.Comment.objects.filter(review=review)
        return queryset

    def perform_create(self, serializer):
        author = self.request.user
        review = get_object_or_404(
            models.Review,
            id=self.kwargs.get('review_id'),
        )
        serializer.save(
            author=author,
            review=review
        )
