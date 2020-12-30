from django.contrib import admin
# Register your models here.
from auction.models import Bid, TeamCaptain, ToBeAuctioned, Joker

admin.site.register(Bid)
admin.site.register(TeamCaptain)
admin.site.register(ToBeAuctioned)
admin.site.register(Joker)