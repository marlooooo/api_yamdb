from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from . import serializers
from reviews import models


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
