# from django.apps import apps
from django.conf import settings

from rest_framework import serializers

# Доступ к моделям через apps.get_model(app_label='review', model_name='User')


User = settings.AUTH_USER_MODEL


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
from rest_framework import serializers

from reviews import models


class ReviewSerializer(serializers.ModelSerializer):
    pass


class CommentSerializer(serializers.ModelSerializer):
    pass
