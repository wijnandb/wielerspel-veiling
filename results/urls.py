from django.urls import path
from . import views

app_name = 'results'


urlpatterns = [path('', views.index, name='index'),
               path('search/', views.SearchResultsView.as_view(), name='search-results'),
               path('results/', views.RaceListView.as_view(), name='index'),
               path('renners/', views.RiderListView.as_view(), name='riders'),
               path('toprenners/', views.TopRiders.as_view(), name='top500'),
               path('renner/<rider>/', views.ResultsListView.as_view(),
                    name='rider-detail'),
               path('editie/<year>/renner/<rider>/', views.ResultsListView.as_view(),
                    name='rider-detail'),
               path('<year>/', views.RaceListView.as_view(), name='races'),
               path('races/', views.RaceListView.as_view(), name='races'),
               path('race/<int:pk>/',
                    views.RaceDetailView.as_view(), name='race-detail'),
               path('ploegen/<year>/', views.PloegleiderListView.as_view(), name='ploegleiders'),
               path('<year>/verkocht/', views.VerkochtListView.as_view(), name='verkochte_renners'),
               path('ploeg/<teamcaptain>/editie/<year>/',
                    views.PloegleiderDetailView.as_view(), name='ploegleider-detail'),
               path('ploeg/<teamcaptain>/',
                    views.PloegleiderDetailView.as_view(), name='ploegleider-detail'),
               path('uitslag/<int:pk>/',
                    views.RaceDetailView.as_view(), name='uitslag-detail'),
               path('teams/<year>/', views.PloegleiderListView.as_view(), name='teams'),
               path('team/<teamcode>/', views.Team.as_view(), name='team-detail'),
               path('country/<country>/', views.Country.as_view(), name='country-detail'),
               
               ]
