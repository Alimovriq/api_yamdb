from django.contrib import admin

from reviews.models import (
    Title,
    Category,
    Genre,
    GenreTitle
)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'description',
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
    )


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'genre',
    )