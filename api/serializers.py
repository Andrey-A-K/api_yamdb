from django.db.models.aggregates import Avg
from rest_framework import serializers
from .models import Comment, Reviews, Titles, Genres, Categories, User, ROLE_CHOICES


class GenresSerializer(serializers.ModelSerializer):
    lookup_field = 'slug'
    extra_kwargs = {
        'url': {'lookup_field': 'slug'}
    }

    class Meta:
        model = Genres
        fields = ('name', 'slug')


class CategoriesSerializer(serializers.ModelSerializer):
    lookup_field = 'slug'
    extra_kwargs = {
        'url': {'lookup_field': 'slug'}
    }

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()

    def get_rating(self, title):
        return title.reviews.aggregate(rating=Avg('score'))['rating']

    class Meta:
        model = Titles
        fields = '__all__'
        # fields = ('id', 'name', 'year', 'rating',
        #           'description', 'genre', 'category')


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


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        fields = '__all__'
        model = User
