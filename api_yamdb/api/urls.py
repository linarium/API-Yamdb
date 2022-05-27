from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register(
    'categories', views.CategoriesViewSet, basename='categories')
router_v1.register('genres', views.GenresViewSet, basename='genres')
router_v1.register('titles', views.TitlesViewSet, basename='titles')
router_v1.register('users', views.UserViewSet, basename='users')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewsViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentsViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/auth/signup/', views.APISignUp.as_view()),
    path('v1/auth/token/', views.APIToken.as_view()),
    path('v1/users/me/', views.APIMeUser.as_view()),
    path('v1/', include(router_v1.urls))
]
