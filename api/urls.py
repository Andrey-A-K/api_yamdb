from django.urls import path
<<<<<<< HEAD
=======
<<<<<<< HEAD
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ReviewsViewSet, CommentViewSet


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

urlpatterns = [
    path('v1/', include(router_v1.urls)),
=======
>>>>>>> df908da128a6df3096ab6e7e678cf6dce37ab081
from django.urls import include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from .views import TitlesViewSet
from .views import CategoriesViewSet
from .views import GenresViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ReviewsViewSet, CommentViewSet

# Создаётся роутер
router = DefaultRouter()
# Связываем URL с viewset, аналогично обычному path()
# В роутере можно зарегистрировать любое количество пар "URL, viewset":
# router.register('categories/<slug:slug>/',
#                 CategoriesViewSet,
#                 basename='category')
router.register('categories', CategoriesViewSet, basename='categories')
router.register('genres', GenresViewSet, basename='genres')
router.register('titles', TitlesViewSet, basename='titles')


urlpatterns = [
    # В список добавляем новый path() с роутером.
    # Все зарегистрированные в router пути доступны в router.urls
    path('v1/', include(router.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
<<<<<<< HEAD
]


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

urlpatterns = [
    path('v1/', include(router_v1.urls)),
=======
>>>>>>> 68454656fb98752b7f6d21a97bdbad61ec58e500
>>>>>>> df908da128a6df3096ab6e7e678cf6dce37ab081
]
