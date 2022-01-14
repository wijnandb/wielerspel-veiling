from django.contrib import admin
from .models import Rider, Category, RacePoints, Race, Uitslag 
from import_export.admin import ImportExportModelAdmin
from import_export import resources


class RiderResource(resources.ModelResource):

    class Meta:
        model = Rider
        import_id_fields = ('cqriderid',)


class RiderAdmin(ImportExportModelAdmin):
    list_display = ('name', 'cqriderid', 'nationality')
    list_filter = ("sold","nationality",)
    search_fields = ['name']
    ordering = ['cqriderid']


class UitslagAdmin(ImportExportModelAdmin):
    list_display = ('race', 'rank', 'rider', 'race_id')
    list_filter = ('race__category', 'rank', 'race__country')
    search_fields = ('race', 'rider')


class RaceAdmin(ImportExportModelAdmin):
    list_display = ('edition', 'name', 'startdate', 'enddate', 'category', 'country')
    list_filter = ('category', 'country')
    search_fields = ('name', 'cqraceid')
    # add link to CQranking site
    # add filter on editie

class RacePointsAdmin(ImportExportModelAdmin):
    list_display = ('category', 'ranking', 'points', 'jpp', 'editie')
    list_filter = ('editie', 'category', 'ranking')


class CategoryAdmin(ImportExportModelAdmin):
    list_display =('name',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Rider, RiderAdmin)
admin.site.register(RacePoints, RacePointsAdmin)
admin.site.register(Race, RaceAdmin)
admin.site.register(Uitslag, UitslagAdmin)
