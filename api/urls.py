from django.urls import path
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ReviewsViewSet, CommentViewSet, TitlesViewSet, CategoriesViewSet, GenresViewSet
from rest_framework.authtoken import views
from .views import CategoriesViewSet, GenresViewSet, TitlesViewSet

from .views import CommentViewSet, ReviewsViewSet

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
urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
]
