from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from .models import Titles, Reviews
from .serializers import CommentSerializer
from .serializers import TitlesReadSerializer
from .serializers import TitlesWriteSerializer
from .serializers import ReviewsSerializer
from rest_framework import permissions

from api.serializers import CategoriesSerializer
from api.serializers import GenresSerializer
from api.models import Titles
from api.models import Categories
from api.models import Genres
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from api.models import User
from api.serializers import UserSerializer

from .permissions import IsAuthorOrReadOnly


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class ModelMixinSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """Класс для дальнейшего наследования."""

    pass


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'genre', 'name', 'year']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitlesReadSerializer
        return TitlesWriteSerializer


class CategoriesViewSet(ModelMixinSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = 'slug'
    filter_backends = [SearchFilter]
    search_fields = ['=name', ]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class GenresViewSet(ModelMixinSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    lookup_field = 'slug'
    filter_backends = [SearchFilter]
    search_fields = ['=name', ]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer

    def get_queryset(self):
        queryset = Reviews.objects.filter(titles__id=self.kwargs.get('titles_id'))
        return queryset

    def perform_create(self, serializer):
        titles = get_object_or_404(Titles, id=self.kwargs['titles_id'],)
        serializer.save(author=self.request.user, titles=titles)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Reviews, id=self.kwargs['review_id'],)
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Reviews,
            id=self.kwargs['review_id'],
            titles__id=self.kwargs['titles_id']
        )
        serializer.save(author=self.request.user, review=review)


class UserVewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly, permissions.IsAdminUser]
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = User.objects.all()
