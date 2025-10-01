# from django.shortcuts import render
# from .models import Destination, Tours
# from django.views.generic import ListView, DetailView
# from django.conf import settings
# from django.contrib import messages


# class DestinationsListView(ListView):
#     model = Destination
#     template_name = 'destinations/dest_list.html'
#     paginate_by = getattr(settings, 'DESTINATIONS_PER_PAGE', 12)

#     def get_queryset(self):
#         queryset = Destination.objects.filter()
