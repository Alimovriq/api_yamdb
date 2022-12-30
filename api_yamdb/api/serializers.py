import datetime as dt

from rest_framework import serializers

from reviews.models import Title, Category


class TitleSerializer(serializers.ModelSerializer):
    """Сериалайзер для произведений."""

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        current_year = dt.date.today().year()
        if value > current_year:
            raise serializers.ValidationError('Проверьте год произведения!')
        return value


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер для категорий."""

    class Meta:
        model = Category
        fields = '__all__'