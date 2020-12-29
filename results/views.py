from django.views import generic
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView


from .models import Rider, Race, Ploegleider, Uitslag, Verkocht


def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_races = Race.objects.all().count()
    num_riders = Rider.objects.count()  # The 'all()' is implied by default.
    num_ploegleiders = Ploegleider.objects.count()
    num_sold_riders = Verkocht.objects.count()


# Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={'num_races': num_races, 'num_riders': num_riders,
                 'num_ploegleiders': num_ploegleiders,
                 'num_sold_riders': num_sold_riders, })


class RaceListView(generic.ListView):
    model = Race
    paginate_by = 30


class RaceDetailView(generic.DetailView):
    model = Race


class RiderListView(generic.ListView):
    model = Rider


class RiderDetailView(generic.DetailView):
    model = Rider


class PloegleiderListView(generic.ListView):
    model = Ploegleider


class PloegleiderDetailView(generic.DetailView):
    model = Ploegleider


class UitslagListView(generic.ListView):
    model = Uitslag


class UitslagDetailView(generic.DetailView):
    model = Uitslag


class VerkochtListView(generic.ListView):
    model = Verkocht
    # I need to be able to filter on Editie (=year)


class VerkochtDetailView(generic.DetailView):
    model = Verkocht
    # I want to use cqriderid as PK
