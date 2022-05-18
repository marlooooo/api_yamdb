from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import year_validator


class User(AbstractUser):
    """Класс, описывающий стандартного пользователя."""
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    Role = (
        (USER, '0'),
        (MODERATOR, '1'),
        (ADMIN, '2'),
    )
    email = models.EmailField(
        'email',
        max_length=254,
        unique=True
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
        default=USER,
        choices=Role,
        max_length=10,
    )

    class Meta:
        constraints = [
            models.constraints.UniqueConstraint(
                fields=('username', 'email'),
                name='user_email_constraint'
            )
        ]
        ordering = ('-id',)

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    def permission_level(self) -> int:
        return int(self.get_role_display())


class Genre(models.Model):
    """Класс, описывающий жанр."""
    name = models.TextField(
        'Название',
        default='Название жанра'
    )
    slug = models.SlugField(
        'id жанра',
        unique=True,
        db_index=True
    )

    class Meta:
        ordering = ('-slug',)

    def __str__(self):
        return self.name


class Category(models.Model):
    """Класс, описывающий категорию"""
    name = models.TextField(
        'Название',
        default='Название категории'
    )
    slug = models.SlugField(
        'id категории',
        unique=True,
        db_index=True
    )

    class Meta:
        ordering = ('-slug',)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Класс, описывающий произведение."""

    name = models.TextField(
        'Название',
        default='Название произведения',
    )
    year = models.IntegerField(
        'Год выпуска',
        validators=[year_validator],
        blank=True,
        null=True,
    )
    description = models.TextField(
        'Описание',
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles'
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    """Класс, описывающий отзывы."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField('Текст отзыва',)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.IntegerField(
        'Оценка',
        validators=(
            MinValueValidator(1, message='Оценка не может быть менее 1'),
            MaxValueValidator(10, message='Оценка не может быть более 10')
        )
    )
    pub_date = models.DateTimeField('Дата и время публикации',
                                    auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='title_author_together'
            )
        ]

    def __str__(self):
        return f'Отзыв на {self.title} от {self.author}'


class Comment(models.Model):
    """Класс, описывающий комментарии."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField('Текст комментария',)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ('id',)
