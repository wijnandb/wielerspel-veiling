from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from auction.models import Bid, TeamCaptain, ToBeAuctioned, Joker, VirtualTeam

class VirtualTeamAdmin(ImportExportModelAdmin):
    list_display = ('editie', 'rider', 'ploegleider', 'price', 'punten', 'jpp')
    list_filter = ('ploegleider', 'editie')


class JokerAdmin(ImportExportModelAdmin):
    list_display = ('team_captain', 'rider', 'value')
    list_filter = ('team_captain',)


class ToBeAuctionedAdmin(ImportExportModelAdmin):
    list_display = ('rider', 'team_captain', 'amount', 'sold')
    list_filter = ('sold', 'created')


admin.site.register(Bid)
admin.site.register(TeamCaptain)
admin.site.register(ToBeAuctioned, ToBeAuctionedAdmin)
admin.site.register(Joker, JokerAdmin)
admin.site.register(VirtualTeam, VirtualTeamAdmin)

