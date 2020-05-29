from django.contrib import admin

from .models import Rider, Category, RacePoints, Race, Ploegleider, Verkocht, Edition, Uitslag, Country


admin.site.register(Category)
admin.site.register(Rider)
admin.site.register(RacePoints)
admin.site.register(Race)
admin.site.register(Ploegleider)
admin.site.register(Verkocht)
admin.site.register(Edition)
admin.site.register(Uitslag)
admin.site.register(Country)
