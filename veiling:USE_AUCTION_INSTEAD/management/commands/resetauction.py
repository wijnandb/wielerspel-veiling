from django.core.management.base import BaseCommand, CommandError

from auction.models import Bid as Bid 
from auction.models import VirtualTeam as VirtualTeam
from results.models import Rider

class Command(BaseCommand):
    """
    WIP: reset only a specific version of the auction, so addd "editie"
    """
    help = 'Careful! Used to reset, empty existing data.'

    def handle(self, *args, **options):
        """
        Empty VirtualTeam, empty Bid, set all Riders to sold = False
        """
        
        sold_riders = Rider.objects.filter(sold=True)
        sold_riders.update(sold=False)
        

        Bid.objects.all().delete()

        VirtualTeam.objects.all().delete()


