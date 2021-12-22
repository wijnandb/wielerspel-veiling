from auction.models import ToBeAuctioned

class OnListToBeAuctioned:

    def get_context(self):
        context = super().get_context_data()
        context['geheimelijst'] = ToBeAuctioned.objects.filter(team_captain=self.request.user)
        return context