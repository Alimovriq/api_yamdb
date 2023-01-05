from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from api.views import (
    TitleViewSet,
    CategoryViewSet,
    GenreViewSet,
    ReviewViewSet,
    UsersViewSet)
from . import views

router_v1 = DefaultRouter()

router_v1.register('titles', TitleViewSet)
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('users', UsersViewSet)
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')

urlpatterns = [
    path('', include(router_v1.urls)),
    path(
        'token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'),
    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'),
    path(
        'token/verify/',
        TokenVerifyView.as_view(),
        name='token_verify'),
    path('auth/signup/', views.signup),
    path('auth/token/', views.token),
]
