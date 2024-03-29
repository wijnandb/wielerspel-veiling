from django.contrib import admin
from .models import Rider, Category, RacePoints, Race, Uitslag, CalculatedPoints
from import_export.admin import ImportExportModelAdmin
from import_export import resources


class RiderResource(resources.ModelResource):

    class Meta:
        model = Rider
        import_id_fields = ('cqriderid',)


class RiderAdmin(ImportExportModelAdmin):
    list_display = ('name', 'cqriderid', 'nationality')
    list_filter = ("team", "sold", "nationality",)
    search_fields = ['name']
    ordering = ['name']


class UitslagAdmin(ImportExportModelAdmin):
    list_display = ('race', 'rank', 'rider', 'race_id')
    list_filter = ('race__category', 'rank', 'race__country')
    search_fields = ('race', 'rider')
    ordering = ('-race__startdate',)


class RaceAdmin(ImportExportModelAdmin):
    list_display = ('editie', 'name', 'startdate', 'enddate', 'category', 'country')
    list_filter = ('category', 'country')
    search_fields = ('name', 'cqraceid')
    ordering = ('-startdate',)
    # add link to CQranking site
    # add filter on editie

class RacePointsAdmin(ImportExportModelAdmin):
    list_display = ('category', 'ranking', 'points', 'jpp', 'editie')
    list_filter = ('editie', 'category', 'ranking')


class CategoryAdmin(ImportExportModelAdmin):
    list_display =('name',)


class CalculatedPointsAdmin(ImportExportModelAdmin):
    list_display =('rider', 'editie', 'points', 'jpp')
    list_filter = ('editie', 'rider')
    search_fields = ('rider',)
    ordering = ('-points',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Rider, RiderAdmin)
admin.site.register(RacePoints, RacePointsAdmin)
admin.site.register(Race, RaceAdmin)
admin.site.register(Uitslag, UitslagAdmin)
admin.site.register(CalculatedPoints, CalculatedPointsAdmin)
