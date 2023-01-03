from django_filters import rest_framework as filters

from reviews.models import Title


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class TitleFilter(filters.FilterSet):
    name = CharFilterInFilter(field_name='name', lookup_expr='in')
    category = CharFilterInFilter(field_name='category__slug')
    genre = CharFilterInFilter(field_name='genre__slug')
    year = filters.RangeFilter()

    class Meta:
        model = Title
        fields = ['name', 'category', 'genre', 'year']
