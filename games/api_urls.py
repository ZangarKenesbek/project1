from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import GameViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'games', GameViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
