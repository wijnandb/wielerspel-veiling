from django.core.management.base import BaseCommand, CommandError
from django.db.models import Sum
from datetime import datetime
import time
from auction.models import Bid, VirtualTeam, ToBeAuctioned, Joker, TeamCaptain
from results.models import Rider
from veiling.views import get_rider_on_auction


class Command(BaseCommand):
    help = 'Checks if bidding is over and sells rider. Keeps running'

    def handle(self, *args, **options):
        """
        This is the function that gets the latest rider that was bid on, finds the
        highest bid on that rider and sells that rider to the highest bidder.
        WIP: check if pause after auctioned rider is working
        USe a site variable in settings to set the Edition (now hardcoded 2021 or 2022 or 2023 )
        """
        # the auction is over when all points have been spend
        # no, when there is only one team_captain left with points
        #punten = VirtualTeam.objects.aggregate(Sum('price'))['price__sum']
        #punten_over = 1400 - punten['price__sum']
        # WIP: replace with solution where we look at # of active teamcaptains.
        while TeamCaptain.objects.aggregate(Sum('riders_proposed'))['riders_proposed__sum']<400:
            print(TeamCaptain.objects.aggregate(Sum('riders_proposed'))['riders_proposed__sum'])
            team_captain, rider_on_auction = get_rider_on_auction()
            #print(f"Totaal {VirtualTeam.objects.count()} verkocht")
            #print(f"Punten besteed: {VirtualTeam.objects.aggregate(Sum('price'))['price__sum']}")
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

                if verschil > 20:
                    latestrider = latest[0].rider
                    #print(latestrider.id)
                    if not VirtualTeam.objects.filter(rider=latestrider, editie=2023).exists():
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
                            if winner.amount < 1:
                                winner.amount = 1
                        #print(winner.rider, winner.team_captain, winner.amount)
                        renner = VirtualTeam()
                        renner.rider = winner.rider
                        renner.team_captain = winner.team_captain
                        renner.price = winner.amount 
                        renner.editie = 2023
                        renner.save()

                        sold_rider = Rider.objects.get(id=winner.rider_id)
                        sold_rider.sold = True
                        sold_rider.save()

                        # update all existing entries for sold rider, set to sold
                        ToBeAuctioned.objects.filter(rider=winner.rider_id).update(sold=True)
                        # add 1 to riders_proposed for teamcaptain who has just proposed a rider
                        # WIP: update team_captains who are allowed to make a bid (so who have points left)

                        proposed_rider_teamcaptain = TeamCaptain.objects.get(team_captain=team_captain)
                        proposed_rider_teamcaptain.riders_proposed += 1
                        proposed_rider_teamcaptain.save()
                        print(f"{latestrider} has been sold to {winner.team_captain} for {winner.amount}")

                    else:
                        print(f'{latestrider} is al verkocht')

                else:
                    print("Nog bezig met bieden")
            else:
                print(f"Wachten op openingsbod van {team_captain.get_full_name()}")
            time.sleep(1)
            # send it in a loop
            # check if all points have been spend
            # make it run again
            # self.handle()
        else:
            print("Veiling is voorbij!")
