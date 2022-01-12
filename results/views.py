from django.views import generic
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models import Sum

from auction.models import TeamCaptain, ToBeAuctioned, User, VirtualTeam
from results.models import Rider, Race, Uitslag


def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_riders = Rider.objects.filter(sold=False).count()  # filter on active=True once field is added
    num_ploegleiders = TeamCaptain.objects.count() # filter on active=True once field is added
    num_sold_riders = VirtualTeam.objects.filter(editie=2022).count()
    if num_sold_riders == 0:
        punten_over = num_ploegleiders * 100
    else:
        punten = VirtualTeam.objects.aggregate(Sum('price'))
        punten_over = num_ploegleiders * 100 - punten['price__sum']

# Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={'num_riders': num_riders,
                 'num_ploegleiders': num_ploegleiders,
                 'num_sold_riders': num_sold_riders, 
                 'punten_over': punten_over})


class RaceListView(generic.ListView):
    model = Race


class RaceDetailView(generic.DetailView):
    model = Race


class RiderListView(generic.ListView):
    model = Rider
    #paginate_by = 500
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['geheimelijst'] = ToBeAuctioned.objects.filter(team_captain=self.request.user)
        return context

    # filter, show only riders that haven't been sold
    def get_queryset(self):
        return Rider.objects.filter(sold=False) #.exclude(tobeauctioned__team_captain=self.request.user)


class TopRiders(RiderListView):
    def get_queryset(self):
        return Rider.objects.filter(sold=False)[0:250]


class RiderDetailView(generic.DetailView):
    model = Rider

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['teamcaptain'] = VirtualTeam.objects.filter(rider=self.object)
        return context    


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

    def get_queryset(self):
        return VirtualTeam.objects.filter(editie=2022)
 

class VerkochtDetailView(generic.DetailView):
    model = VirtualTeam

