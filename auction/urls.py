from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import LoginView, ToBeAuctionedListView, TeamCaptainListView, JokerListView
from .views import AddRiderToBeAuctioned, SaveOrderingToBeAuctioned, RemoveRiderToBeAuctioned, SoldRider

app_name = 'auction'

urlpatterns = [
    path('geheimelijst/', ToBeAuctionedListView.as_view(), name='geheimelijst'),
    path('aanbiedvolgorde/', TeamCaptainListView.as_view(), name='aanbiedvolgorde'),
    path('jokers/', JokerListView.as_view(), name='jokers'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page='auction:login'), name='logout'),
    path('ajax/add_rider_tobeauctioned/', AddRiderToBeAuctioned, name='ajax-add-rider-tobeauctioned'),
    path('ajax/remove_rider_tobeauctioned/', RemoveRiderToBeAuctioned, name='ajax-remove-rider-tobeauctioned'),
    path('ajax/sort_rider_tobeauctioned', SaveOrderingToBeAuctioned, name='ajax-save-ordering-tobeauctioned'),
    path('ajax/sold_rider/', SoldRider, name="ajax-sold-rider"),
]
