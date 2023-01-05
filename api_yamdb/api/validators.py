from rest_framework.exceptions import ValidationError
from django.core.validators import RegexValidator
from users.models import User


username_validator = RegexValidator(
    r"^[\w.@+-]+\Z",
    'Введите иное имя пользователя')


def validate_username(value):
    if User.objects.filter(username=value).exists():
        raise ValidationError('Пользователь с таким именем '
                              'уже существует')
    elif value == 'me':
        raise ValidationError('Запрещено использовать me в качестве имени!')


def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError('Пользователь с такой почтой '
                              'уже существует')
