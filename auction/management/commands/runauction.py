from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
import time
from auction.models import Bid, VirtualTeam, ToBeAuctioned, Joker 
from results.models import Rider

class Command(BaseCommand):
    help = 'Checks if bidding is over and sells rider. Keeps running'

    def handle(self, *args, **options):
        """
        This is the function that gets the latest rider that was bid on, finds the
        highest bid on that rider and sells that rider to the highest bidder.
        WIP: check if pause after auctioned rider is working
        USe a site variable in settings to set the Edition (now hardcoded 2021 or 2022)
        """
        # first, check what the latest bid was
        latest = Bid.objects.order_by('-created')
        # get the rider that was bidded on
        # could be improved by checking on latest unsold rider
        if latest:
            Timestamp = latest[0].created
            #print(Timestamp)
            #print(type(Timestamp))
            nu=datetime.now()
            #print(nu)
            #print(type(nu))
            #print((nu-Timestamp).total_seconds())
            verschil = ((nu-Timestamp).total_seconds())
            #print(verschil)
            # I want to know if the latest bid has been
            # at least x seconds ago. If that is the case, the
            # bidding should be closed and the rider goes to the
            # highest bidder. 

            if verschil > 20:
                latestrider = latest[0].rider
                print(latestrider.id)
                if not VirtualTeam.objects.filter(rider=latestrider, editie=2022).exists():
                    # print(latestrider)
                    # get the highest bid on that rider
                    # extra sort on created, so we get the Joker bid (same value, later entry) 
                    highest = Bid.objects.filter(rider=latestrider).order_by('-amount', '-created')
                    # check if there is a Joker
                    winner=highest[0]
                    if Joker.objects.filter(rider=latestrider).exists():
                        joker = Joker.objects.get(rider=latestrider)
                    
                        if winner.team_captain == joker.team_captain:
                            winner.amount = winner.amount + joker.value
                        if winner.amount <= 0:
                            winner.amount = 1
                    print(winner.rider, winner.team_captain, winner.amount)
                    renner = VirtualTeam()
                    renner.rider = winner.rider
                    renner.ploegleider = winner.team_captain
                    renner.price = winner.amount 
                    renner.editie = 2022
                    renner.save()

                    sold_rider = Rider.objects.get(id=winner.rider_id)
                    sold_rider.sold = True
                    sold_rider.save()

                    verkocht_rider = ToBeAuctioned.objects.get(rider=winner.rider_id)
                    verkocht_rider.sold = True
                    verkocht_rider.save()
                    # Pause before new rider gets auctioned
                    time.sleep(5)

                else:
                    print(f'{latestrider} is al verkocht')

            else:
                print("Nog bezig met bieden")
        else:
            print(f"Nog geen biedingen aanwezig")
        time.sleep(1)
        # make it run again
        # Wip WIP WIP WIP WIP
        # turn on auction at specified time
        # built in a PAUSE button?
        # WHO controls PAUSE button?
        # uncomment line below to start auction (and run python manage.py runauction)
        self.handle()
