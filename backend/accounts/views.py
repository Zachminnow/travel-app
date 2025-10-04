from django.views import generic
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    # Redirect to the login page on successful signup
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
