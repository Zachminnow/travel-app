from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DestinationViewSet, TourViewSet

router = DefaultRouter()
router.register(r'destinations', DestinationViewSet, basename='destination')
router.register(r'tours', TourViewSet, basename='tour')

urlpatterns = [
    path('api/', include(router.urls)),
]
