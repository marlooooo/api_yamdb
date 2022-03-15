from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Класс, описывающий стандартного пользователя."""
    class Role(models.Choices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

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
        'biography',
        blank=True,
        null=True,
    )
    role = models.CharField(
        'role',
        default=Role.USER,
        choices=Role.choices,
        max_length=10,
    )
