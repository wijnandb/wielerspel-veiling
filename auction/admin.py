from django.contrib import admin
# Register your models here.
from auction.models import Bid, TeamCaptainStatus

admin.site.register(Bid)
admin.site.register(TeamCaptainStatus)