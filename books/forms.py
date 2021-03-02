from django import forms

from .models import Ticket, Review, UserFollows


class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = [
            'title',
            'description',
            'image',
        ]
        labels = {
            "title": "Titre",
            "description": "Description",
            "image": "Image",
        }


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = [
            'headline',
            'rating',
            'body',
        ]
        labels = {
            "headline": "Description",
            "rating": "Note",
            "body": "Contenu",
        }


class UserFollowsForm(forms.ModelForm):

    class Meta:
        model = UserFollows
        fields = [
            'followed_user',
        ]
