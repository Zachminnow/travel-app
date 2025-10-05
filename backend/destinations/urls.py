from django.urls import path
from . import views

urlpatterns = [
    # Destination url
    path('destination/', views.DestinationListView.as_view(),
         name='destination_list'),
    path('destinations/create/', views.DestinationCreateView.as_view(),
         name='destination_create'),
    path('destinations/<slug:slug>/',
         views.DestinationDetailView.as_view(), name='destination_detail'),
    path('destinations/<slug:slug>/edit/',
         views.DestinationUpdateView.as_view(), name='destination_update'),
    path('destinations/<slug:slug>/delete/',
         views.DestinationDeleteView.as_view(), name='destination_delete'),

    # Tour urls
    path('tours/', views.TourListView.as_view(), name='tour_list'),
    path('tours/create/', views.TourCreateView.as_view(), name='tour_create'),
    path('tours/<slug:slug>/', views.TourDetailView.as_view(),
         name='tour_detail'),
    path('tours/<slug:slug>/edit/',
         views.TourUpdateView.as_view(), name='tour_update'),
    path('tours/<slug:slug>/delete/',
         views.TourDeleteView.as_view(), name='tour_delete'),
]
