
class YearFilterMixin:

    def get_queryset(self):
        queryset = super(YearFilterMixin, self).get_queryset()
        year = self.kwargs.get('year', 2022)
        return queryset.filter(editie=year)
    
    # def get_context(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     year = self.kwargs.get('year', 2022)
    #     context['year'] = year
    #     return context

class TeamCaptainMixin:

    def get_queryset(self):
        queryset = super(TeamCaptainMixin, self).get_queryset()

        teamcaptain = self.request.GET.get('tc')
        if teamcaptain:
            return queryset.filter(team_captain=teamcaptain)
        return queryset
