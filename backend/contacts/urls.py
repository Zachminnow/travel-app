from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactViewSet, OfficeLocationViewSet

router = DefaultRouter()
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'locations', OfficeLocationViewSet, basename='location')

app_name = 'contacts'

urlpatterns = [
    path('', include(router.urls)),
]
