from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

from datetime import datetime


class User(AbstractUser):
    """Класс, описывающий стандартного пользователя."""
    class Role(models.TextChoices):
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


class Genre(models.Model):
    '''Класс, описывающий жанр'''
    name = models.TextField(
        'Название',
        default='Название жанра'
    )
    slug = models.SlugField(
        'id жанра',
        unique=True
    )

    def __str__(self):
        return self.name



class Category(models.Model):
    '''Класс, описывающий категорию'''
    name = models.TextField(
        'Название',
        default='Название категории'
    )
    slug = models.SlugField(
        'id категории',
        unique=True
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    '''Класс, описывающий произведение'''
    name = models.TextField(
        'Название',
        default='Название произведения'
    )
    year = models.IntegerField(
        'Год выпуска',
        validators=(MaxValueValidator(datetime.now().year),),
        blank=True,
        null=True,
    )
    # rating =
    description = models.TextField(
        'Описание',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    '''Класс, описывающий отзывы'''
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
    score = models.IntegerField('Оценка', validators=(MinValueValidator(1),
                                MaxValueValidator(10)))
    pub_date = models.DateTimeField('Дата и время публикации',
                                    auto_now_add=True)

    class Meta:
        unique_together = ('title', 'author')

    def __str__(self):
        return f'Отзыв на {self.title} от {self.author}'


class Comment(models.Model):
    '''Класс, описывающий комментарии'''
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
    pub_date = models.DateTimeField('Дата и время публикации',
                                    auto_now_add=True)
