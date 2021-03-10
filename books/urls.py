from django.urls import path

from . import views

app_name = 'books'
urlpatterns = [
    path(
        route='',
        view=views.FeedView.as_view(),
    ),
    path(
        route='feed/',
        view=views.FeedView.as_view(),
        name='feed',
    ),
    path(
        route='posts/',
        view=views.PostsView.as_view(),
        name='posts',
    ),
    path(
        route='add_ticket/',
        view=views.TicketCreateView.as_view(),
        name='add_ticket'
    ),
    path(
        route='subscriptions/',
        view=views.sub,
        name='sub'
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
        'update/ticket/<int:pk>/',
        views.TicketUpdateView.as_view(),
        name='update_ticket',
    ),
    path(
        'delete/ticket/<int:pk>/',
        views.TicketDeleteView.as_view(),
        name='delete_ticket',
    ),
    path(
        'update/review/<int:pk>/',
        views.ReviewUpdateView.as_view(),
        name='update_review',
    ),
    path(
        'delete/review/<int:pk>/',
        views.ReviewDeleteView.as_view(),
        name='delete_review',
    ),
]
