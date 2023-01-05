import datetime as dt

from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.exceptions import ValidationError

from reviews.models import Title, Category, Genre, Review, User
from .validators import (
    validate_email,
    validate_username,
    username_validator,)


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

    class Meta:
        model = Title
        fields = 'id', 'name', 'year', 'description', 'genre', 'category'

    def validate_year(self, value):
        current_year = dt.date.today().year
        if value > current_year:
            raise serializers.ValidationError('Проверьте год произведения!')
        return value


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
            raise serializers.ValidationError(
                'Проверьте, что score от 0 до 10!'
            )
        return value


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        allow_blank=False,
        validators=[validate_email])
    username = serializers.CharField(
        max_length=150,
        allow_blank=False,
        validators=[validate_username, username_validator])

    class Meta:
        model = User
        fields = (
            'email',
            'username'
        )


class AdminCreationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        allow_blank=False,
        validators=[validate_email])
    username = serializers.CharField(
        max_length=150,
        allow_blank=False,
        validators=[validate_username, username_validator])

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class MeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        allow_blank=False,
        validators=[validate_email])
    username = serializers.CharField(
        max_length=150,
        allow_blank=False,
        validators=[validate_username, username_validator])
    first_name = serializers.CharField(
        max_length=150,
        allow_blank=True)
    last_name = serializers.CharField(
        max_length=150,
        allow_blank=True)

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'bio'
        )


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        allow_blank=False,
        validators=[validate_username, username_validator])
    confirmation_code = serializers.CharField(allow_blank=False,)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )

    def validate(self, value):
        user = get_object_or_404(User, username=value['username'])
        confirmation_code = default_token_generator.make_token(user)
        if str(confirmation_code) != value['confirmation_code']:
            raise ValidationError('Неверный код подтверждения')
        return value
