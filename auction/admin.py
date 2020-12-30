from django.contrib import admin
# Register your models here.
from auction.models import Bid, TeamCaptain

admin.site.register(Bid)
admin.site.register(TeamCaptain)