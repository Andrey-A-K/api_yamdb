from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from .models import Titles, Reviews
from .serializers import (
    CommentSerializer,
    ReviewsSerializer
)
from rest_framework import permissions
from api.serializers import TitlesSerializer
from api.serializers import CategoriesSerializer
from api.serializers import GenresSerializer
from api.models import Titles
from api.models import Categories
from api.models import Genres
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'genre', 'name', 'year']


class CategoriesViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = 'slug'
    filter_backends = [SearchFilter]
    search_fields = ['=name', ]


class GenresViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    lookup_field = 'slug'
    filter_backends = [SearchFilter]
    search_fields = ['=name', ]


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer

    def get_queryset(self):
        titles = get_object_or_404(Titles, id=self.kwargs['titles_id'],)
        return titles.reviews.all()

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
