from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import LoginView, RegistrationView,  \
    ToBeAuctionedListView, AddRiderToBeAuctioned, SaveOrderingToBeAuctioned

app_name = 'auction'

urlpatterns = [
    #path('auction/', AuctionView.as_view(), name='auction'),
    path('geheimelijst/', ToBeAuctionedListView.as_view(), name='geheimelijst'),
    #path('bidding/', bidding, name='bidding'),
    #path('biddings/', biddings, name='biddings'),
    #path('bidding/current/', get_current, name='get_current_bid'),
    #path('bidding/highest/', get_highest, name='get_highest'),
    #path('accounts/registration/', RegistrationView.as_view(), name='register'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page='auction:login'), name='logout'),
    path('ajax/add_rider_tobeauctioned/', AddRiderToBeAuctioned, name='ajax-add-rider-tobeauctioned'),
    path('ajax/sort_rider_tobeauctioned', SaveOrderingToBeAuctioned, name='ajax-save-ordering-tobeauctioned'),
]
