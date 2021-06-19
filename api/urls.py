from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import (CategoriesViewSet, CommentViewSet, UserVewSet,
                    GenresViewSet, LoginAPIView, RegistrationAPIView,
                    ReviewsViewSet, TitlesViewSet, UserRetrieveUpdateAPIView)

router_v1 = DefaultRouter()
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='api_reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='api_comments'
)
router_v1.register('titles', TitlesViewSet, basename='titles')
router_v1.register('categories', CategoriesViewSet, basename='categories')
router_v1.register('genres', GenresViewSet, basename='genres')
router_v1.register('users', UserVewSet, basename='users')
urlpatterns = [
    path('v1/', include(router_v1.urls)),
    # path('user', UserRetrieveUpdateAPIView.as_view()),
    # path('v1/users/', RegistrationAPIView.as_view()),
    # path('v1/users/login/', LoginAPIView.as_view()),
    # path('v1/api-token-auth/', views.obtain_auth_token),
]
