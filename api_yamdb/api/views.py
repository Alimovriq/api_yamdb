from rest_framework import viewsets, mixins, filters
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Title, Category
from .serializers import TitleSerializer, CategorySerializer


class CreateListDeleteViewSet(mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    """Вьюсет для GET, POST, DELETE методов."""

    pass


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для Произведений."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('category',)
