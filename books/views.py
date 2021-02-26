from operator import attrgetter

from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator


from .models import Ticket, Review, UserFollows
from .forms import TicketForm, ReviewForm, UserFollowsForm


class HomeView(LoginView):
    template_name = 'books/home.html'


class TicketListView(LoginRequiredMixin, TemplateView):

    template_name = 'books/ticket_list.html'
    context_object_name = 'feed_items'

    def get_context_data(self):
        tickets = list(Ticket.objects.all())
        reviews = list(Review.objects.all())
        for review in reviews:
            review.rating = range(review.rating)
        feed_items = tickets + reviews
        feed_items.sort(key=attrgetter('time_created'), reverse=True)
        paginator = Paginator(feed_items, 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'page_obj': page_obj,
        }
        return context


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    fields = ['title', 'description', 'image']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReviewAddView(LoginRequiredMixin, TemplateView):
    template_name = 'books/review_form.html'
    context_object_name = 'forms_'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_ticket = TicketForm()
        form_review = ReviewForm()
        context['form_ticket'] = form_ticket
        context['form_review'] = form_review
        return context


def add_review(request, id_ticket=None):
    if id_ticket is not None:
        ticket = get_object_or_404(Ticket.objects, pk=id_ticket)
        if ticket.completed:
            return redirect('tickets')
    else:
        ticket = None
    if request.method == "GET":
        form_review = ReviewForm()
        form_ticket = TicketForm()
        context = {
            'ticket': ticket,
            'form_review': form_review,
            'form_ticket': form_ticket,
        }
        if id_ticket:
            context['id_ticket'] = id_ticket
        return render(request, 'books/review_form.html', context)

    elif request.method == 'POST':
        form_ticket = TicketForm()
        if not ticket:
            ticket_data = {
                'title': request.POST['title'],
                'description': request.POST['description'],
            }
            form_ticket = TicketForm(ticket_data)
            if request.FILES:
                form_ticket.instance.image = request.FILES['image']
            form_ticket.instance.user = request.user

        review_data = {
            'headline': request.POST['headline'],
            'rating': request.POST['rating'],
            'body': request.POST['body'],
        }
        form_review = ReviewForm(review_data)
        form_review.instance.user = request.user

        if (ticket or form_ticket.is_valid()) and form_review.is_valid():
            if ticket:
                ticket.completed = True
                ticket.save()
                form_review.instance.ticket = ticket
            else:
                form_ticket.instance.completed = True
                form_ticket.save()
                form_review.instance.ticket = Ticket.objects.last()
            form_review.save()
            return redirect('tickets')
        else:
            context = {
                'ticket': ticket,
                'form_review': form_review,
                'form_ticket': form_ticket,
            }
            if id_ticket:
                context['id_ticket'] = id_ticket
            return render(request, 'books/review_form.html', context)


def sub(request):
    follows = []
    followed_by = []
    follow_list = []
    if UserFollows.objects.filter(user=request.user):
        for entry in UserFollows.objects.filter(user=request.user):
            follows.append(entry.followed_user)
    if UserFollows.objects.filter(followed_user=request.user):
        for entry in UserFollows.objects.filter(followed_user=request.user):
            followed_by.append(entry.user)
    follow_list = [user for user in User.objects.all()
                   if user not in follows and user != request.user]
    if request.method == 'GET':
        context = {
            'follow_list': follow_list,
            'follows': follows,
            'followed_by': followed_by,
        }
        return render(request, 'books/sub.html', context)
    if request.method == 'POST':
        if request.POST.get('followed_user'):
            new_followed_user = User.objects.get(
                pk=request.POST['followed_user'])
            new_user = request.user
            new_entry = UserFollows(
                user=new_user, followed_user=new_followed_user)
            new_entry.save()
            return redirect('sub') 
        elif request.POST.get('delete'):
            UserFollows.objects.get(
                followed_user=User.objects.get(id=request.POST['delete'])
                ).delete()
            return redirect('sub')
