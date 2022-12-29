from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    """Модель категория."""

    name = models.CharField(
        'Название',
        max_length=256
    )
    slug = models.SlugField(
        unique=True,
        max_length=50
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


# Написать модельки Жанров и Категорий, привязать к Произведениям,
# учесть их связь и удаление.
class Title(models.Model):
    """Модель произведение."""

    name = models.CharField(
        'Название',
        max_length=256
    )
    year = models.IntegerField(
        'Год'
    )
    description = models.TextField(
        'Описание',
        null=True
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        related_name='titles'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


# class Review(models.Model):
#     author = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name='comments')
#     title = models.ForeignKey(
#         Title, on_delete=models.CASCADE, related_name='comments')
#     text = models.TextField()
#     pub_date = models.DateTimeField(
#         'Дата добавления', auto_now_add=True, db_index=True)
#     score = models.IntegerField()


# class Comment(models.Model):
#     author = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name='comments')
#     review = models.ForeignKey(
#         Review, on_delete=models.CASCADE, related_name='comments')
#     text = models.TextField()
#     pub_date = models.DateTimeField(
#         'Дата добавления', auto_now_add=True, db_index=True)