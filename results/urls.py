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
               path('races/<year>/', views.RaceListView.as_view(), name='races'),
               path('races/', views.RaceListView.as_view(), name='races'),
               path('race/<int:pk>/',
                    views.RaceDetailView.as_view(), name='race-detail'),
               path('race/<int:pk>/edit/',
                    views.RaceEditView.as_view(), name='race-edit'),
               path('ploegen/<year>/', views.PloegleiderListView.as_view(), name='ploegleiders'),
               path('verkocht/<year>/', views.VerkochtListView.as_view(), name='verkochte_renners'),
               path('ploeg/<teamcaptain>/editie/<year>/',
                    views.PloegleiderDetailView.as_view(), name='ploegleider-detail'),
               path('ploeg/<teamcaptain>/',
                    views.PloegleiderDetailView.as_view(), name='ploegleider-detail'),
               path('uitslag/<int:pk>/',
                    views.RaceDetailView.as_view(), name='uitslag-detail'),
               path('teams/', views.TeamListView.as_view(), name='teams'),
               path('team/<teamcode>/', views.Team.as_view(), name='team-detail'),
               path('country/<country>/', views.Country.as_view(), name='country-detail'),
               path('categories/', views.CategoryListView.as_view(), name='points'),
               path('category/<int:pk>/<year>/', views.CategoryDetailView.as_view(), name='category-detail'),
               path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
               path('geheimelijst/<year>/', views.PointsEarnedListView.as_view(), name="geheimelijst"),
               #path('geheimelijst/', views.PointsEarnedListView.as_view(), name="geheimelijst"),
               path('stand/', views.PloegLeiderStand.as_view(), name='stand',)
               ]
