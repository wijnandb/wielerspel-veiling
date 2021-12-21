from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from auction.models import Bid, TeamCaptain, ToBeAuctioned, Joker, VirtualTeam, AuctionOrder

class VirtualTeamAdmin(ImportExportModelAdmin):
    list_display = ('rider', 'ploegleider', 'price', 'punten', 'jpp')
    list_filter = ('ploegleider', 'editie')


class JokerAdmin(ImportExportModelAdmin):
    list_display = ('team_captain', 'rider', 'value')
    list_filter = ('team_captain',)


class ToBeAuctionedAdmin(ImportExportModelAdmin):
    list_display = ('order', 'rider', 'team_captain', 'amount', 'sold')
    list_filter = ('team_captain', 'sold', 'modified', 'created')

class AuctionOrderAdmin(ImportExportModelAdmin):
    list_display = ('team_captain', 'order')


admin.site.register(Bid)
admin.site.register(TeamCaptain)
admin.site.register(ToBeAuctioned, ToBeAuctionedAdmin)
admin.site.register(Joker, JokerAdmin)
admin.site.register(VirtualTeam, VirtualTeamAdmin)
admin.site.register(AuctionOrder, AuctionOrderAdmin)

