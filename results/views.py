from itertools import groupby
from django.views.generic import ListView, DetailView, UpdateView
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Sum, Count

from auction.models import TeamCaptain, ToBeAuctioned, User, VirtualTeam
from results.models import CalculatedPoints, Category, Rider, Race, Uitslag, RacePoints

from core.views import YearFilterMixin, TeamCaptainMixin


def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_riders = Rider.objects.filter(sold=False).exclude(rank__isnull=True).count()  # filter on active=True once field is added
    num_ploegleiders = TeamCaptain.objects.count() # filter on active=True once field is added
    num_sold_riders = VirtualTeam.objects.filter(editie=2023).count()
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


class TeamListView(ListView):
    model = Rider
    template_name = 'results/teams.html'

    def get_queryset(self):
        #return Rider.objects.order_by('team').distinct('team').annotate(rider_count=Count('team'))
        return Rider.objects.all().annotate(numberriders=Count('team')).order_by('team')
        #return Rider.objects.distinct('team').annotate(numberriders=Count('team'))


class RaceListView(YearFilterMixin, ListView):
    model = Race
    #paginate_by = 25


class RaceDetailView(DetailView):
    model = Race


class RaceEditView(UpdateView):
    model = Race
    fields = '__all__'
    template_name = "results/update_form.html"

    success_url = '/categories/'


class RiderListView(ListView):
    model = Rider
    #paginate_by = 100


    # filter, show only riders that haven't been sold
    def get_queryset(self):
        return Rider.objects.exclude(rank__isnull=True) #.exclude(tobeauctioned__team_captain=self.request.user)

class SoldRiderListView(RiderListView):

    def get_queryset(self):
        return Rider.objects.filter(sold=True, editie=2023)


class TopRiders(RiderListView):
    def get_queryset(self):
        return Rider.objects.filter(sold=False)[0:250]


class Team(RiderListView):

    def get_queryset(self, *args, **kwargs):
        team = self.kwargs['teamcode']
        return Rider.objects.filter(team=team).filter(sold=False)


class Country(RiderListView):

    def get_queryset(self, **kwargs):
        country = self.kwargs['country']
        return Rider.objects.filter(nationality=country).filter(sold=False).exclude(rank=None)


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
    #template_name = "ploegleider_list.html"
    queryset = VirtualTeam.objects.filter(editie=2023)
    
    # def get_queryset(self, **kwargs):
    #     #tc = self.kwargs.get('teamcaptain', 1)
    #     editie = self.kwargs.get('year', 2022)
        

class PloegLeiderStand(PloegleiderListView):
    template_name = 'results/ploegleider_list.html'
    queryset = VirtualTeam.objects.filter(editie=2023).values_list('team_captain',)\
        .annotate(earned_points=Sum('punten'), earned_jpp=Sum('jpp')).\
            extra(order_by=['-earned_points', '-earned_jpp'])


class PloegleiderDetailView(YearFilterMixin, TeamCaptainMixin, ListView):
    model = VirtualTeam

    def get_queryset(self, **kwargs):
        tc = self.kwargs.get('teamcaptain', 1)
        editie = self.kwargs['year']
        return VirtualTeam.objects.filter(team_captain=tc).filter(editie=editie)
    

class UitslagListView(ListView):
    model = Uitslag
    #paginate_by: 50


class UitslagDetailView(DetailView):
    model = Uitslag
    paginate_by: 30
    #qs.select_related()


class VerkochtListView(YearFilterMixin, TeamCaptainMixin, ListView):
    model = VirtualTeam
    #paginate_by = 30


class VerdienendListView(YearFilterMixin, ListView):
    model = Rider
    paginate_by = 30


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
        years = Uitslag.objects.filter(rider_id=self.kwargs['rider']).values('race__editie').distinct('race__editie').order_by('-race__editie')
        context['years'] = years
        return context


class SearchResultsView(YearFilterMixin, ListView):
    model = Rider
    template_name = "rider-list.html"

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = Rider.objects.filter(name__icontains=query)
        return object_list


class CategoryListView(ListView):
    model = Category


class CategoryDetailView(DetailView):
    model = Category

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data()
    #     context['points'] = RacePoints.objects.filter(category=self)
    #     return context


class PointsEarnedListView(ListView):
    model = CalculatedPoints
    paginate_by = 500
    template_name = "results/geheimelijst.html"
    #paginate_by = 50

    def get_queryset(self, **kwargs):
        # nothing 
        #list2020 = CalculatedPoints.objects.filter(editie__in={2020}).filter(points__gte=1).exclude(rider_id=13543)
        #list2021 = CalculatedPoints.objects.filter(editie__in={2021}).filter(points__gte=1).exclude(rider_id=13543)
        #riders = Rider.objects.filter(rank__gte=0)
        object_list = CalculatedPoints.objects.filter(editie=2022).exclude(rider__rank=None).order_by('rider__rank')
        return object_list#, list2020, list2021

    # def get_context_data(self, *args, **kwargs):
    #     context = super(PointsEarnedListView, self).get_context_data(*args, **kwargs)
    #     context['results2020'] = CalculatedPoints.objects.filter(editie=2020).filter(points__gte=1).exclude(rider_id=13543)
    #     context['results2021'] = CalculatedPoints.objects.filter(editie=2021).filter(points__gte=1).exclude(rider_id=13543)
    #     context['results2022'] = CalculatedPoints.objects.filter(editie=2022).filter(points__gte=1).exclude(rider_id=13543)
    #     return context 

"""
Slimme(re) manier om renners te vinden van ene uitslagenprovider naar de andere: 
naam opslitsen in losse woorden, als eerste woord gelijk aan eerste woord, 
dan tweede woord vergelijken met tweede woord en evntueel meer.

Kijk goed naar de renners bij wie het niet goed gaat, zodat je weet waar het misgaat.
"""
