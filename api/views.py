from api.serializers import TitlesSerializer
from api.serializers import CategoriesSerializer
from api.serializers import GenresSerializer
from api.models import Titles
from api.models import Categories
from api.models import Genres
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'genre', 'name', 'year']


class CategoriesViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'del']
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', ]


class GenresViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'del']
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', ]
