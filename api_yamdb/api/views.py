from django.apps import apps
from django.conf import settings as cfg
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, pagination, filters, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.mixins import (
    ListModelMixin, CreateModelMixin, DestroyModelMixin
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from reviews import models
from . import serializers
from .filters import TitleFilter
from .mixins import CreateMixin, GetOneMixin
from .permissions import (
    AdminOrReadOnly, OwnerOrReadOnly, UserViewSetPermission, CustomIsAuthorized
)

User = apps.get_model(app_label='reviews', model_name='User')


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (UserViewSetPermission,)
    pagination_class = pagination.PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

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

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(
            self.get_queryset(),
            username=kwargs.get('pk')
        )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # @action(
    #     url_path='me',
    #     detail=True,
    #     methods=['GET', 'PATCH'],
    #     permission_classes=(IsAuthenticated, AllowAny),
    # )
    # def me(self, request):
    #     serializer = serializers.UserSerializer(request.user, many=False)
    #     return Response(serializer.data)


class GetMeViewSet(GetOneMixin):
    serializer_class = serializers.UserSerializer
    permission_classes = (CustomIsAuthorized,)
    queryset = User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = request.user
        return Response(self.get_serializer(instance).data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.request.user
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class UserCreationViewSet(CreateMixin):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserCreationSerializer

    def perform_create(self, serializer):
        user = User.objects.get_or_create(
            username=self.request.data.get('username'),
            email=self.request.data.get('email')
        )
        token = Token.objects.create(user=user)
        send_mail(
            subject='ACCESS TOKEN',
            message=f'{token.key}',
            from_email=cfg.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )


class TokenObtainView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        if not User.objects.filter(
                username=request.data.get('username')
        ).exists():
            return Response(
                {"errors": "Пользователь не найден"},
                status=status.HTTP_404_NOT_FOUND
            )
        user = User.objects.filter(username=request.data.get('username'))
        conformation_code = request.data.get('conformation_code')
        valid_code = Token.objects.get(user=user)
        if valid_code.key != conformation_code:
            return Response(
                {"errors": "не правильный код подтверждения"},
                status=status.HTTP_400_BAD_REQUEST
            )
        token = AccessToken.for_user(user)
        serializer = serializers.TokenSerializer(token)
        if serializer.is_valid():
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )




class GenreViewSet(viewsets.GenericViewSet, ListModelMixin, CreateModelMixin,
                   DestroyModelMixin):
    """Вьюсет для жанров"""
    permission_classes = (AdminOrReadOnly,)
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)


class CategoryViewSet(viewsets.GenericViewSet, ListModelMixin,
                      CreateModelMixin, DestroyModelMixin):
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
        if (models.Review.objects.filter(author=author, title=title).exists()):
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
        review = get_object_or_404(models.Review,
                                   id=self.kwargs.get('review_id'))
        queryset = models.Comment.objects.filter(review=review)
        return queryset

    def perform_create(self, serializer):
        author = self.request.user
        review = get_object_or_404(models.Review,
                                   id=self.kwargs.get('review_id'))
        serializer.save(
            author=author,
            review=review
        )
