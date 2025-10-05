from django.urls import reverse_lazy
import logging
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q, Count
from .models import Destination, Tour
from typing import Any
from .forms import DestinationForm, TourForm
from django.contrib import messages
from django.views.generic import ListView, DetailView, View, CreateView, UpdateView, DeleteView


logger = logging.getLogger('travel')


class DestinationListView(ListView):
    model = Destination
    template_name = 'destinations/destination_list.html'
    context_object_name = 'destinations'
    pagination = 12

    def get_queryset(self):
        queryset = Destination.objects.filter(is_active=True)

        # Search functionality
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(country__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        return queryset.annotate(package_count=Count('tours'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['featured_destinations'] = Destination.objects.filter(
            is_featured=True,
            is_active=True
        )[:4]

        return context


class DestinationDetailView(DetailView):
    """View single destination with packages"""
    model = Destination
    template_name = 'destinations/detail.html'
    context_object_name = 'destination'
    slug = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Destination.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        destination = self.get_object()

        # Get tours in the destination
        context['tours'] = Tour.objects.filter(
            destination=destination,
            is_active=True
        )
        context['tours_count'] = context['tours'].count()

        # Related destinations
        context['related_destinations'] = Destination.objects.filter(
            country=destination.country,
            is_active=True
        ).exclude(id=destination.id)[:4]

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


class DestinationCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Create new destination (admin only)"""
    model = Destination
    form_class = DestinationForm
    template_name = 'destinations/form.html'
    permission_required = 'travel.add_destination'

    def form_valid(self, form):
        logger.info(
            f"New destination created: {form.instance.name}",
            extra={'user': self.request.user.id}
        )
        messages.success(self.request, 'Destination created succcessfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.warning(
            f"Destination creation failed",
            extra={'user': self.request.user.id, 'errors': form.errors}
        )
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


class DestinationUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Update existing destionation (admin only)"""
    model = Destination
    form_class = DestinationForm
    template_name = 'destination/form.html'
    permission_required = 'travel.change_destination'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        logger.info(
            f"Destination updated: {form.instance.name}",
            extra={'user': self.request.user.id}
        )
        messages.success(self.request, 'Destination updates successfully!')
        return super().form_valid(form)


class DestinationDeleteView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Update existing destination (admin only)"""
    model = Destination
    template_name = 'destinations/confirm_delete.html'
    success_url = reverse_lazy('destination_list')
    permission_required = 'travel.delete_destination'
    slug = 'slug'
    slug_url_kwarg = 'slug'

    def delete(self, request, *args, **kwargs):
        destination = self.get_object()
        logger.warning(
            f"Destination deleted: {destination.name}",
            extra={'user': request.user.id}
        )
        messages.success(request, 'Destination deleted successfully!')
        return super().delete(request, *args, **kwargs)


class TourListView(ListView):
    """List all active tours"""
    model = Tour
    template_name = 'destination/tours/list.html'
    context_object_name = 'tours'
    paginate_by = 12

    def get_queryset(self):
        queryset = Tour.objects.filter(
            is_active=True
        ).select_related('destination')

        # Filter by destination
        destination_slug = self.request.GET.get('destination')
        if destination_slug:
            queryset = queryset.filter(destination_slug=destination_slug)

        # Filter by type
        tour_type = self.request.GET.get('type')
        if tour_type:
            queryset = queryset.filter(tour_type=tour_type)

        # Search query
        search_query = self.request.GET.get('q')
        queryset = queryset.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
        # Sorting
        sort_by = self.request.GET.get('sort', '-created_at')
        queryset = queryset.order_by(sort_by)

        return queryset

    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['destinations'] = Destination.objects.filter(is_active=True)
        context['tour_types'] = Tour.TOUR_TYPES
        context['selected_destination'] = self.request.GET.get(
            'destination', '')
        context['selected_type'] = self.request.GET.get('type', '')
        context['search_query'] = self.request.GET.get('q', '')

        return context


class TourDetailView(DetailView):
    """View single tour details"""
    model = Tour
    template_name = 'destinations/tours/detail.html'
    context_object_name = 'package'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Tour.objects.filter(
            is_active=True
        ).select_related('destination')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tour = self.get_object()

        # Related tours
        context['related_tours'] = Tour.objects.filter(
            destination=tour.destination,
            is_active=True
        ).exclude(id=tour.id)[:4]

        # User-specific data
        if self.request.user.is_authenticated:
            pass
        return context


class TourCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Tour
    template_name = 'destinations/tours/form.html'
    form_class = TourForm
    permission_required = 'travel.add_tour'

    def form_valid(self, form):
        logger.info(
            f"Tour created succesfully.{form.instance.title}",
            extra={
                'user': self.request.user.id,
                'destination': form.instance.destination.name}
        )
        messages.success(self.request, 'Tour created successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.warning(
            f"Tour creation failed",
            extra={'user': self.request.user.id, 'errors': form.errors}
        )
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


class TourUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Tour
    form_class = TourForm
    template_name = 'destination/tours/form.html'
    permission_required = 'travel.change_tour'
    slug = 'slug'
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        logger.info(
            f"Tour updated: {form.instance.title}",
            extra={'user': self.request.user.id}
        )
        messages.success(self.request, 'Tour updated successfully.')
        return super().form_valid(form)


class TourDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Tour
    template_name = 'destination/tours/confirm_delete.html'
    success_url = reverse_lazy('tour_list')
    permission_required = 'travel.delete_tour'
    slug = 'slug'
    slug_url_kwarg = 'slug'

    def delete(self, request, *args, **kwargs):
        tour = self.get_object()
        logger.warning(
            f"Tour delete: {tour.title}",
            extra={'user': request.user.id}
        )
        messages.error(request, 'Tour deleted succcessfully')
        return super().delete(request, *args, **kwargs)
