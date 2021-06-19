from django.contrib.auth import authenticate
from django.db.models.aggregates import Avg
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import (ROLE_CHOICES, Categories, Comment, Genres, Reviews,
                     Titles, User)


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

    def get_rating(self, obj):
        Titles.objects.annotate(rating=Avg('reviews__score')).all()

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')


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


class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'username', 'bio', 'email', 'role', 'token']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        fields = ['first_name', 'last_name',
                  'username', 'bio', 'email', 'role']
        model = User

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
            instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    # password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        # password = data.get('password', None)
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )
        user = authenticate(username=email)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['confirmation_code'] = serializers.CharField(required=True)
        self.fields.pop('password')

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['confirmation_code'] = self.user.confirmation_code
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
