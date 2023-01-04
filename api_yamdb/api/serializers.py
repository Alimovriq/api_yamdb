import datetime as dt

from django.db.models import Sum
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Title, Category, Genre, Review, Comment


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер для категорий."""

    class Meta:
        model = Category
        fields = 'name', 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер для жанров."""

    class Meta:
        model = Genre
        fields = 'name', 'slug'


class TitleSerializer(serializers.ModelSerializer):
    """Сериалайзер для произведений."""
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = 'id', 'name', 'year', 'description', 'genre', 'category', 'rating'

    def validate_year(self, value):
        current_year = dt.date.today().year
        if value > current_year:
            raise serializers.ValidationError('Проверьте год произведения!')
        return value

    def get_rating(self, obj):
        reviews = Review.objects.filter(title_id = obj.id)
        try:
            reviews[0]
        except Exception:
            return 0
        else:
            rating = reviews.aggregate(Sum("score"))
            return rating["score__sum"]


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


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)
