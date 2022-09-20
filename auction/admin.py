from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from auction.models import Bid, TeamCaptain, ToBeAuctioned, Joker, VirtualTeam

class VirtualTeamAdmin(ImportExportModelAdmin):
    list_display = ('editie', 'rider', 'team_captain', 'price', 'punten', 'jpp')
    list_filter = ('team_captain', 'editie')


class JokerAdmin(ImportExportModelAdmin):
    list_display = ('team_captain', 'rider', 'value')
    list_filter = ('team_captain',)


class ToBeAuctionedAdmin(ImportExportModelAdmin):
    list_display = ('order', 'rider', 'team_captain', 'amount', 'sold')
    list_filter = ('team_captain', 'sold', 'modified', 'created')

class TeamCaptainAdmin(ImportExportModelAdmin):
    list_display = ('team_captain_id', 'team_captain', '__str__', 'order', 'riders_proposed')


admin.site.register(Bid)
admin.site.register(TeamCaptain, TeamCaptainAdmin)
admin.site.register(ToBeAuctioned, ToBeAuctionedAdmin)
admin.site.register(Joker, JokerAdmin)
admin.site.register(VirtualTeam, VirtualTeamAdmin)
