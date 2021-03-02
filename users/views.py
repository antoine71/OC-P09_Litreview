from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView


class HomeView(LoginView):
    template_name = 'users/home.html'


class UserLogoutView(LogoutView):
    template_name = 'users/logout.html'


class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'users/register_form.html'

    def get_success_url(self):
        return reverse_lazy('users:register_confirmation')


class RegistrationConfirmationView(TemplateView):
    template_name = 'users/register_confirmation.html'
