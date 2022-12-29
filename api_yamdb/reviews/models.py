from django.db import models


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

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
