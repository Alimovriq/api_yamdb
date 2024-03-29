# Generated by Django 3.2 on 2023-01-05 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20221230_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'Администратор'), ('user', 'Аутентифицированный пользователь'), ('moderator', 'Модератор')], default='user', max_length=50, verbose_name='Роль'),
        ),
    ]
