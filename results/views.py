from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Sum

from auction.models import TeamCaptain, ToBeAuctioned, User, VirtualTeam
from results.models import CalculatedPoints, Rider, Race, Uitslag

from core.views import YearFilterMixin, TeamCaptainMixin


def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_riders = Rider.objects.filter(sold=False).exclude(rank__isnull=True).count()  # filter on active=True once field is added
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


class RaceListView(YearFilterMixin, ListView):
    model = Race
    paginate_by = 25


class RaceDetailView(DetailView):
    model = Race


class RiderListView(ListView):
    model = Rider
    paginate_by = 100


    # filter, show only riders that haven't been sold
    #def get_queryset(self):
    #    return Rider.objects.filter(sold=False).exclude(rank__isnull=True) #.exclude(tobeauctioned__team_captain=self.request.user)

class SoldRiderListView(RiderListView):

    def get_queryset(self):
        return Rider.objects.filter(sold=True, editie=2022)


class TopRiders(RiderListView):
    def get_queryset(self):
        return Rider.objects.filter(sold=False)[0:250]


class Team(RiderListView):

    def get_queryset(self, *args, **kwargs):
        team = self.kwargs['teamcode']
        return Rider.objects.filter(team=team)


class Country(RiderListView):

    def get_queryset(self, **kwargs):
        country = self.kwargs['country']
        return Rider.objects.filter(nationality=country)


class RiderDetailView(DetailView):
    model = Rider

    # def get_queryset(self, **kwargs):
    #     year = self.kwargs['year']
    #     return Rider.objects.filter(nationality=country)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['teamcaptain'] = VirtualTeam.objects.filter(rider=self.object)
        return context    


class PloegleiderListView(ListView):
    model = VirtualTeam
    template_name = 'ploegleider_list.html'

    def get_queryset(self, **kwargs):
        tc = self.kwargs['teamcaptain']
        editie = self.kwargs['year']
        return VirtualTeam.objects.filter(team_captain=tc).filter(editie=editie)


class PloegleiderDetailView(YearFilterMixin, TeamCaptainMixin, ListView):
    model = VirtualTeam

    def get_queryset(self, **kwargs):
        tc = self.kwargs['teamcaptain']
        editie = self.kwargs['year']
        return VirtualTeam.objects.filter(team_captain=tc).filter(editie=editie)
    

class UitslagListView(ListView):
    model = Uitslag
    #paginate_by: 50


class UitslagDetailView(DetailView):
    model = Uitslag
    paginate_by: 25
    #qs.select_related()


class VerkochtListView(YearFilterMixin, TeamCaptainMixin, ListView):
    model = VirtualTeam


class VerkochtDetailView(DetailView):
    model = VirtualTeam


class ResultsListView(ListView):
    model = Uitslag
    template_name = "rider-results.html"
    year = '2022'

    def get_queryset(self):
        rider = self.kwargs['rider']
        year = self.kwargs.get('year', self.year)
        return Uitslag.objects.filter(rider=rider, race__startdate__year=year)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['rider'] = Rider.objects.get(id=self.kwargs['rider'])
        context['year'] = self.kwargs.get('year', self.year)
        return context


class SearchResultsView(YearFilterMixin, ListView):
    model = Rider
    template_name = "rider-list.html"

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = Rider.objects.filter(name__icontains=query)
        return object_list

def ComparePoints(request):
    """
    Get all sold riders and for each rider get both the calculated value and the value from

    """
    
    pass