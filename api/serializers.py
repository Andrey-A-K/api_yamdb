from rest_framework import serializers
<<<<<<< HEAD
from django.contrib.auth import get_user_model
from .models import Comment, Reviews

from .models import Genres
from .models import Titles
from .models import Categories
=======
from .models import Comment, Reviews, Titles, Genres, Categories
>>>>>>> df908da128a6df3096ab6e7e678cf6dce37ab081

User = get_user_model()


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


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = '__all__'
        model = Reviews


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = '__all__'
        model = Comment
