from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from auction.models import Bid, TeamCaptain, ToBeAuctioned, Joker, VirtualTeam

class VirtualTeamAdmin(ImportExportModelAdmin):
    list_display = ('rider', 'ploegleider', 'price', 'punten', 'jpp')
    list_filter = ('ploegleider', 'editie')


class JokerAdmin(ImportExportModelAdmin):
    list_display = ('team_captain', 'rider', 'value')
    list_filter = ('team_captain',)


admin.site.register(Bid)
admin.site.register(TeamCaptain)
admin.site.register(ToBeAuctioned)
admin.site.register(Joker, JokerAdmin)
admin.site.register(VirtualTeam, VirtualTeamAdmin)

