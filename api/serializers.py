from rest_framework import serializers
from .models import Comment, Reviews, Titles, Genres, Categories, User, ROLE_CHOICES


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


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROLE_CHOICES)
    usesr = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = User
