from django.urls import path

from . import views

urlpatterns = [
    path(
        route='',
        view=views.HomeView.as_view(redirect_authenticated_user=True),
        name='home',
    ),
    path(
        route='tickets/',
        view=views.TicketListView.as_view(),
        name='tickets',
    ),
    path(
        route='add_ticket/',
        view=views.TicketCreateView.as_view(),
        name='add_ticket'
    ),
    path(
        route='add_review/',
        view=views.add_review,
        name='add_review'
    ),
    path(
        route='add_review/<int:id_ticket>/',
        view=views.add_review,
        name='add_review'
    ),
    path(
        route='sub/',
        view=views.sub,
        name='sub'
    ),
]
