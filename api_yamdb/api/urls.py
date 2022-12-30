from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (
    TitleViewSet,
    CategoryViewSet,
    GenreViewSet,
    ReviewViewSet)

router_v1 = DefaultRouter()

router_v1.register('titles', TitleViewSet)
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')

urlpatterns = [
    path('', include(router_v1.urls)),
]
