from django.urls import path
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ReviewsViewSet, CommentViewSet, TitlesViewSet, CategoriesViewSet, GenresViewSet


router_v1 = DefaultRouter()
router = DefaultRouter()
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
]
