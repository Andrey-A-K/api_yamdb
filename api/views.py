from django_filters.rest_framework import DjangoFilterBackend
from .utils import email_is_valid, generate_mail
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django.contrib.auth.tokens import default_token_generator
from rest_framework import permissions
from .filters import TitleFilter
from rest_framework.response import Response
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action, api_view, permission_classes
from .permissions import (
    IsAdmin, IsAdminUserOrReadOnly, IsModerator, IsOwner, IsUser
)
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
)
from .models import Titles, Reviews, Titles, Categories, Genres
from .serializers import (
    CommentSerializer,
    ReviewsSerializer,
    GenresSerializer,
    TitlesReadSerializer,
    CategoriesSerializer,
    TitlesCreateSerializer,
    UserSerializer
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


class ModelMixinSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """Класс для дальнейшего наследования."""

    pass


class CategoriesViewSet(ModelMixinSet):
    pagination_class = PageNumberPagination
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = 'slug'
    filter_backends = [SearchFilter]
    search_fields = ['name', ]
    permission_classes = [IsAdminUserOrReadOnly]


class GenresViewSet(ModelMixinSet):
    pagination_class = PageNumberPagination
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    lookup_field = 'slug'
    filter_backends = [SearchFilter]
    search_fields = ['name', ]
    permission_classes = [IsAdminUserOrReadOnly]


class TitlesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = Titles.objects.all().annotate(Avg('reviews_title__score'))
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    filterset_fields = ['name', 'category', 'genre', 'year']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitlesReadSerializer
        return TitlesCreateSerializer


class ReviewCommentMixin(viewsets.ModelViewSet):
    permission_classes = [IsOwner]
    permission_classes_by_action = {'list': [AllowAny],
                                    'create': [IsUser | IsAdmin | IsModerator],
                                    'retrieve': [AllowAny],
                                    'partial_update': [IsOwner],
                                    'destroy': [IsAdmin | IsModerator]}

    def get_permissions(self):
        try:
            return [permission() for permission
                    in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class ReviewsViewSet(ReviewCommentMixin):
    pagination_class = PageNumberPagination
    serializer_class = ReviewsSerializer

    def get_queryset(self):
        queryset = Reviews.objects.filter(
            title__id=self.kwargs.get('title_id')
        )
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, pk=self.kwargs['title_id'],)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ReviewCommentMixin):
    pagination_class = PageNumberPagination
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


class UserVewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated,
                          permissions.IsAdminUser]
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = User.objects.all()
