from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from api.models import Categories, Genres, Reviews, Titles, User
from api.serializers import (CategoriesSerializer, CommentSerializer,
                             GenresSerializer, ReviewsSerializer,
                             TitlesSerializer, UserSerializer)

from .permissions import IsAuthorOrReadOnly


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'genre', 'name', 'year']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CategoriesViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = 'slug'
    filter_backends = [SearchFilter]
    search_fields = ['=name', ]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class GenresViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
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
