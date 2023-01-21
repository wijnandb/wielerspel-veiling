from django.urls import path
from .views import AuctionView, bidding, get_current, biddings, \
    get_highest, get_rider_on_auction

app_name = 'veiling'

urlpatterns = [
    path('', AuctionView.as_view(), name='veiling'),
    #path('geheimelijst/', ToBeAuctionedListView.as_view(), name='geheimelijst'),
    path('bidding/', bidding, name='bidding'),
    path('biddings/', biddings, name='biddings'),
    path('bidding/current/', get_current, name='get_current_bid'),
    path('bidding/highest/', get_highest, name='get_highest'),
    path('getrider', get_rider_on_auction, name='get_rider_on_auction'),
]