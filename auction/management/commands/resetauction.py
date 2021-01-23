from django.core.management.base import BaseCommand, CommandError

from auction.models import Bid as Bid 
from auction.models import VirtualTeam as VirtualTeam
from auction.models import ToBeAuctioned as ToBeAuctioned 
from results.models import Rider

class Command(BaseCommand):
    help = 'Carteful! Used to reset, empty existing data'

    def handle(self, *args, **options):
        """
        Empty VirtualTeam, empty Bid, set all Riders to sold = False
        Set all riders in ToBeAuctioned to sold = False 
        """
        
        sold_riders = Rider.objects.filter(sold=True)
        sold_riders.update(sold=False)

        verkocht_riders = ToBeAuctioned.objects.filter(sold=True)
        verkocht_riders.update(sold=False)
        

        Bid.objects.all().delete()

        VirtualTeam.objects.all().delete()
