
class YearFilterMixin:

    def get_queryset(self):
        queryset = super(YearFilterMixin, self).get_queryset()
        
        year = self.request.GET.get('year')
        if year:
            return queryset.filter(editie=year)
        return queryset

class TeamCaptainMixin:

    def get_queryset(self):
        queryset = super(TeamCaptainMixin, self).get_queryset()

        teamcaptain = self.request.GET.get('tc')
        if teamcaptain:
            return queryset.filter(ploegleider=teamcaptain)
        return queryset
