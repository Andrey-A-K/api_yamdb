from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action, api_view, permission_classes
from .permissions import IsAdmin, IsAdminUserOrReadOnly
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from .models import Titles, Reviews, Titles, Categories, Genres
from .serializers import (
    CommentSerializer,
    ReviewsSerializer,
    GenresSerializer,
    TitlesSerializer,
    TitleCreateSerializer,
    CategoriesSerializer,
    UserSerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from .utils import email_is_valid, generate_mail
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser | IsAdmin]
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = [SearchFilter]
    search_fields = ['username', ]

    @action(methods=['patch', 'get'], detail=False,
            permission_classes=[IsAuthenticated],
            url_path='me', url_name='me')
    def me(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                instance, data=request.data, partial=True)
            serializer.is_valid()
            serializer.save()
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def send_confirmation_code(request):
    email = request.data.get('email')
    if email is None:
        message = 'Электронная почта обязательна'
    else:
        if email_is_valid(email):
            user = get_object_or_404(User, email=email)
            confirmation_code = default_token_generator.make_token(user)
            generate_mail(email, confirmation_code)
            user.confirmation_code = confirmation_code
            message = email
            user.save()
        else:
            message = 'Требуется действующий адрес электронной почты'
    return Response({'email': message})


class TitlesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUserOrReadOnly, ]
    queryset = Titles.objects.all().annotate(Avg('reviews__score'))
    serializer_class = TitlesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'genre', 'name', 'year']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitlesSerializer
        return TitleCreateSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUserOrReadOnly, ]
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
        queryset = Reviews.objects.filter(
            title__id=self.kwargs.get('titles_id')
        )
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, pk=self.kwargs['titles_id'],)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Reviews, pk=self.kwargs['review_id'],)
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Reviews,
            pk=self.kwargs['review_id'],
            title__id=self.kwargs['title_id']
        )
        serializer.save(author=self.request.user, review=review)
