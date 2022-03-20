from django.urls import path, include
from rest_framework import routers

from . import views

router_v1 = routers.DefaultRouter()
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    'reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    'comments'
)

router_v1.register(
    'categories',
    views.CategoryViewSet,
    'categories',
)

router_v1.register(
    'genres',
    views.GenreViewSet,
    'genres',
)

router_v1.register(
    'titles',
    views.TitleViewSet,
    'titles',
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
