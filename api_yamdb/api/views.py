from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Title
from .serializers import TitleSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для Произведений."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
