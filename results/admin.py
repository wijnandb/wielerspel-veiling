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


class UitslagAdmin(ImportExportModelAdmin):
    list_display = ('race', 'rank', 'rider', 'race_id')
    list_filter = ('race', 'rank')
    search_fields = ('race', 'rider')


class RaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'startdate', 'category', 'country')
    list_filter = ('category', 'country')
    search_fields = ('race', 'rider')
    # add link to CQranking site
    # add filter on editie


admin.site.register(Category)
admin.site.register(Rider, RiderAdmin)
admin.site.register(RacePoints)
admin.site.register(Race, RaceAdmin)
admin.site.register(Uitslag, UitslagAdmin)
