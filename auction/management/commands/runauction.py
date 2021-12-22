from django.core.management.base import BaseCommand, CommandError
from django.db.models import Sum
from datetime import datetime
import time
from auction.models import Bid, VirtualTeam, ToBeAuctioned, Joker, TeamCaptain 
from results.models import Rider


teamcaptains_to_propose = [1,2,3,4,5,6]
class Command(BaseCommand):
    help = 'Checks if bidding is over and sells rider. Keeps running'

    def handle(self, *args, **options):
        """
        This is the function that gets the latest rider that was bid on, finds the
        highest bid on that rider and sells that rider to the highest bidder.
        """
        # the auction is over when all points have been spend
        # no, when there is only one team_captain left with points
        #punten = VirtualTeam.objects.aggregate(Sum('price'))['price__sum']
        #punten_over = 1400 - punten['price__sum']

        while VirtualTeam.objects.aggregate(Sum('price'))['price__sum']<1400:
            #print(f"Totaal {VirtualTeam.objects.count()} verkocht")
            print(f"Punten besteed: {VirtualTeam.objects.aggregate(Sum('price'))['price__sum']}")
            # first, check what the latest bid was
            latest = Bid.objects.order_by('-created')
            # get the rider that was bidded on
            # could be improved by checking on latest unsold rider
            # this decides IF we are going to auction a rider, as well as WHICH rider we will auction
            # I could use this to create a pause and select a new rider. Right?
            # Or should that be done  
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
                # at least 10 seconds ago. If that is the case, the
                # bidding should be closed and the rider goes to the
                # highest bidder. 

                if verschil > 10:
                    latestrider = latest[0].rider
                    print(latestrider.id)
                    if not VirtualTeam.objects.filter(rider=latestrider, editie=2022).exists():
                        # print(latestrider)
                        # get the highest bid on that rider
                        # extra sort on created, so we get the Joker bid (same value, later entry)
                        # a bit crappy, better to look for highest bid, then check if there is a (highest) bid
                        # from a team_captain holding a joker
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

                        # update all existing entries for sold rider, set to sold
                        ToBeAuctioned.objects.filter(rider=winner.rider_id).update(sold=True)
                        #verkocht_rider.sold = True
                        #verkocht_rider.save()
                        print(f"{latestrider} has been sold to {winner.team_captain} for {winner.amount}")

                    else:
                        print(f'{latestrider} is al verkocht')

                else:
                    print("Nog bezig met bieden")
            else:
                print(f"Nog geen biedingen aanwezig")
            time.sleep(1)
            # send it in a loop
            # check if all points have been spend
            # make it run again
            # self.handle()
        else:
            print("Veiling is voorbij!")
