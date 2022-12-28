from django.db import models


class Title(models.Model):
    """Модель произведение."""

    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(null=True)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
