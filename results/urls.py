from django.urls import path
from . import views

app_name = 'results'


urlpatterns = [path('', views.index, name='index'),
               path('renners/', views.RiderListView.as_view(), name='riders'),
               path('renner/<int:cqriderid>', views.RiderDetailView.as_view(),
                    name='rider-detail'),
               path('races/', views.RaceListView.as_view(), name='races'),
               path('race/<int:pk>',
                    views.RaceDetailView.as_view(), name='race-detail'),
               path('ploegen/', views.PloegleiderListView.as_view(), name='ploegleiders'),
               path('verkocht/', views.VerkochtListView.as_view(), name='verkochte_renners'),
               path('ploeg/<int:pk>',
                    views.PloegleiderDetailView.as_view(), name='ploegleider-detail'),
               path('uitslagen/', views.RaceListView.as_view(), name='uitslagen'),
               path('uitslag/<int:pk>',
                    views.RaceDetailView.as_view(), name='uitslag-detail'),
               ]
