from django.urls import path

from . import views


app_name = 'users'
urlpatterns = [
    path(
        route='home/',
        view=views.HomeView.as_view(redirect_authenticated_user=True),
        name='home',
    ),
    path(
        'register/',
        view=views.UserCreateView.as_view(),
        name='register'),
    path(
        'register/confirmation',
        view=views.RegistrationConfirmationView.as_view(),
        name='register_confirmation'),
    path(
        'login/',
        view=views.HomeView.as_view(),
        name='login'),
    path(
        'logout/',
        view=views.UserLogoutView.as_view(),
        name='logout'),
]
