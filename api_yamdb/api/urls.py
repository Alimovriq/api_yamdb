from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import TitleViewSet, CategoryViewSet

router_v1 = DefaultRouter()

router_v1.register('titles', TitleViewSet)
router_v1.register('categories', CategoryViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
]
