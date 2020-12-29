from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import LoginView, AuctionView, RegistrationView, AuctionListView, bidding, get_current, biddings, \
    get_highest

app_name = 'auction'

urlpatterns = [
    path('auction', AuctionListView.as_view(), name='bids'),
    path('auction/<rider_id>', AuctionView.as_view(), name='auction'),
    path('bidding', bidding, name='bidding'),
    path('biddings', biddings, name='biddings'),
    path('bidding/current', get_current, name='get_current_bid'),
    path('bidding/highest', get_highest, name='get_highest'),
    path('accounts/registration', RegistrationView.as_view(), name='register'),
    path('accounts/login', LoginView.as_view(), name='login'),
    path('accounts/logout', LogoutView.as_view(next_page='auction:login'), name='logout'),
]