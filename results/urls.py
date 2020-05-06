from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('riders/', views.RiderListView.as_view(), name='riders'),
    path('rider/<int:pk>', views.RiderDetailView.as_view(),
         name='rider-detail'),
    path('races/', views.RaceListView.as_view(), name='races'),
    path('race/<int:pk>',
         views.RaceDetailView.as_view(), name='race-detail'),
    path('ploegen/', views.PloegleiderListView.as_view(), name='teams'),
    path('ploeg/<int:pk>',
         views.PloegleiderDetailView.as_view(), name='team-detail'),
]
