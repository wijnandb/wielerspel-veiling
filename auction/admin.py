from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from auction.models import Bid, TeamCaptain, ToBeAuctioned, Joker, VirtualTeam

class VirtualTeamAdmin(ImportExportModelAdmin):
    list_display = ('rider', 'ploegleider', 'price', 'punten', 'jpp')
    list_filter = ('ploegleider', 'editie')

admin.site.register(Bid)
admin.site.register(TeamCaptain)
admin.site.register(ToBeAuctioned)
admin.site.register(Joker)
admin.site.register(VirtualTeam, VirtualTeamAdmin)

