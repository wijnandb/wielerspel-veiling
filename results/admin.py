from django.contrib import admin
from .models import Rider, Category, RacePoints, Race, Ploegleider, Verkocht, Edition, Uitslag, Country


class RiderAdmin(admin.ModelAdmin):
    list_display = ('name', 'cqriderid', 'nationality')
    list_filter = ("nationality",)
    search_fields = ['name']


class VerkochtAdmin(admin.ModelAdmin):
    list_display = ('rider', 'ploegleider', 'price', 'punten', 'jpp')
    list_filter = ('ploegleider', 'editie')


class UitslagAdmin(admin.ModelAdmin):
    list_display = ('race', 'rank', 'rider')
    list_filter = ('race', 'rank')
    search_fields = ('race', 'rider')


admin.site.register(Category)
admin.site.register(Rider, RiderAdmin)
admin.site.register(RacePoints)
admin.site.register(Race)
admin.site.register(Ploegleider)
admin.site.register(Verkocht, VerkochtAdmin)
admin.site.register(Edition)
admin.site.register(Uitslag, UitslagAdmin)
admin.site.register(Country)
