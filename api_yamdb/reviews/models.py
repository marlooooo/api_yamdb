from django.db import models
from django.contrib.auth.models import AbstractUser


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


class Title(models.Model):
    pass


class Review(models.Model):
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
    score = models.IntegerField('Оценка', )
    pub_date = models.DateTimeField('Дата и время публикации',
                                    auto_now_add=True)

    class Meta:
        unique_together = ('title', 'author')

    def __str__(self):
        return f'Отзыв на {self.title} от {self.author}'


class Comment(models.Model):
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
