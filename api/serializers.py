from rest_framework import serializers

from .models import Genres
from .models import Titles
from .models import Categories


class GenresSerializer(serializers.ModelSerializer):
    lookup_field = 'slug'
    extra_kwargs = {
        'url': {'lookup_field': 'slug'}
    }

    class Meta:
        model = Genres
        fields = ('name', 'slug', 'genre')


class CategoriesSerializer(serializers.ModelSerializer):
    lookup_field = 'slug'
    extra_kwargs = {
        'url': {'lookup_field': 'slug'}
    }

    class Meta:
        model = Categories
        fields = ('name', 'slug', 'category')


class TitlesSerializer(serializers.ModelSerializer):
    genre = GenresSerializer(many=True, required=False)
    category = CategoriesSerializer(many=True, required=False)

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
