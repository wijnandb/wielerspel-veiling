from django.views import generic
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from auction.models import TeamCaptain, User
from django.db.models import Sum


from .models import Rider, Race, Uitslag
from auction.models import VirtualTeam


def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_riders = Rider.objects.count()  # The 'all()' is implied by default.
    num_ploegleiders = User.objects.count()
    num_sold_riders = VirtualTeam.objects.count()
    punten = VirtualTeam.objects.aggregate(Sum('price'))
    punten_besteed = 1500- punten['price__sum']


# Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={'num_riders': num_riders,
                 'num_ploegleiders': num_ploegleiders,
                 'num_sold_riders': num_sold_riders, 
                 'punten_besteed': punten_besteed})


class RaceListView(generic.ListView):
    model = Race
    paginate_by = 30


class RaceDetailView(generic.DetailView):
    model = Race


class RiderListView(generic.ListView):
    model = Rider
    # filter, show only riders that haven't been sold
    def get_queryset(self):
          return Rider.objects.filter(sold=False)

class RiderDetailView(generic.DetailView):
    model = Rider


class PloegleiderListView(generic.ListView):
    model = TeamCaptain


class PloegleiderDetailView(generic.DetailView):
    model = TeamCaptain


class UitslagListView(generic.ListView):
    model = Uitslag


class UitslagDetailView(generic.DetailView):
    model = Uitslag


class VerkochtListView(generic.ListView):
    model = VirtualTeam
    # I need to be able to filter on Editie (=year)


class VerkochtDetailView(generic.DetailView):
    model = VirtualTeam
