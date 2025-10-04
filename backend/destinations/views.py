from typing import Any
from .forms import DestinationForm
from django.contrib import messages
from django.views.generic import ListView, DetailView, View
from .models import Destination, Tour


class DestinationListView(ListView):
    model = Destination
    template_name = 'destinations/destination_list.html'
    context_object_name = 'destinations'
    queryset = Destination.objects.all().order_by('-pickup_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class Home(View):
    template_name = 'destinations/home.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["featured_destinations"] = Destination.objects.filter(
            is_featured=True)
        context['all_destinations'] = Destination.objects.filter.all()
        context['tours'] = Tour.objects.all()

        return context
