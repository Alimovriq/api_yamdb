import datetime as dt

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Title, Category, Review


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
        
        
class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title',)

    def validate_score(self, value):
        if value < 0 or value > 10:
            raise serializers.ValidationError('Проверьте, что score от 0 до 10!')
        return value
 
