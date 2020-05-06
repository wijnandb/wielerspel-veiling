from django.views import generic

from .models import Rider, Race, Ploegleider


def index(request):
    pass


class IndexView(generic.ListView):
    template_name = 'index.html'


class RaceListView(generic.ListView):
    model = Race
    paginate_by = 30


class RaceDetailView(generic.DetailView):
    model = Race


class RiderListView(generic.ListView):
    model = Rider
    paginate_by = 30


class RiderDetailView(generic.DetailView):
    model = Rider


class PloegleiderListView(generic.ListView):
    model = Ploegleider


class PloegleiderDetailView(generic.DetailView):
    model = Ploegleider
