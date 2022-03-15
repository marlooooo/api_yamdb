from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Класс, описывающий стандартного пользователя."""
    class Role(models.IntegerChoices):
        user = 0
        moderator = 1
        admin = 2

    email = models.EmailField(
        'email',
        max_length=254,
    )
    first_name = models.CharField(
        'first name',
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        'last name',
        max_length=150,
        blank=True,
    )
    bio = models.TextField(
        blank=True,
        null=True,
    )
    role = models.CharField(
        max_length=255,
        default='user',
        null=True,
        blank=True,
        choices=Role.choices,
    )
