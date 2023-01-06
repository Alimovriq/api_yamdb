from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, filters, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator


from reviews.models import (
    Title,
    Category,
    Genre,
    User,
    Review)
from .serializers import (
    AdminCreationSerializer,
    TitleSerializer,
    TitleViewSerializer,
    CategorySerializer,
    GenreSerializer,
    MeSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TokenSerializer,
    CommentSerializer)
from .permissions import (
    AdminOrReadOnly,
    AdminOnly,
    AdminOrModeratorOrAuthor,
    UserIsAuthor)

from .filters import TitleFilter


class CreateListDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """Вьюсет для GET, POST, DELETE методов."""
    permission_classes = [
        AdminOrReadOnly
    ]
    pass


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = [AdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleViewSerializer
        return TitleSerializer


class CategoryViewSet(CreateListDestroyViewSet):
    """Вьюсет для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def destroy(self, *args, **kwargs):
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenreViewSet(CreateListDestroyViewSet):
    """Вьюсет для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def destroy(self, *args, **kwargs):
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        try:
            Review.objects.get(title_id=title_id, author=self.request.user)
        except Exception:
            title = get_object_or_404(Title, id=title_id)
            serializer.save(author=self.request.user, title=title)
        else:
            raise Exception("Можно оставить только один отзыв!")


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminCreationSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = LimitOffsetPagination
    permission_classes = [AdminOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(detail=False, methods=['get', 'patch', 'post'],
            permission_classes=[UserIsAuthor, IsAuthenticated])
    def me(self, request):
        user = get_object_or_404(
            User,
            username=self.request.user.username
        )
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = MeSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            if 'role' in request.data:
                if user.role != 'user':
                    serializer.save()
            else:
                serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    user = get_or_none(
        User,
        username=request.data.get('username'),
        email=request.data.get('email'))
    if user is None:
        serializer.is_valid(raise_exception=True)
        if not User.objects.filter(username=request.data['username'],
                                   email=request.data['email']).exists():
            serializer.save()
        user = User.objects.get(username=request.data['username'],
                                email=request.data['email'])
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            f'Привет, {str(user.username)}! Твой код подтверждения ниже!',
            confirmation_code,
            settings.EMAIL_FOR_AUTH_LETTERS,
            [request.data['email']],
            fail_silently=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        serializer.is_valid()
        user = User.objects.get(username=request.data['username'],
                                email=request.data['email'])
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            f'Привет, {str(user.username)}! Твой код подтверждения ниже!',
            confirmation_code,
            settings.EMAIL_FOR_AUTH_LETTERS,
            [request.data['email']],
            fail_silently=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def tokens_for_user(user):
    tokens = RefreshToken.for_user(user)
    refresh = str(tokens)
    access = str(tokens.access_token)
    data = {
        "refresh": refresh,
        "access": access
    }
    return data


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=request.data['username'])
    confirmation_code = request.data['confirmation_code']
    if default_token_generator.check_token(user, confirmation_code):
        token = tokens_for_user(user)
        response = {'token': str(token['access'])}
        return Response(response, status=status.HTTP_200_OK)
    return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)
