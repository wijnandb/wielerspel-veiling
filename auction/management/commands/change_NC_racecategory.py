from django.core.management.base import BaseCommand, CommandError

from auction.models import VirtualTeam 
from results.models import Race, Category

import time

class Command(BaseCommand):
    help = 'Calculate the points a rider has accumulated and store it somewhere'

    def handle(self, *args, **options):
        """
        Categories whose points are dependent on sold riders per country/continent in that year:
        NC1=14, NC2=15  NC3=16  NC4=17   NC5=18 
        NCT1 through NCT5: 19, 20, 21, 22,23
        # do these manually, or even hardcoded: if Europe, then WT1.3
        CC1, CC2, CCT1, CCT2: 24, 25, 26, 27 

        """
        # select all races with a category in a list
        to_be_adjusted = Race.objects.filter(category__in=[14,15,16,17,18,19,20,21,22,23])
        for tbd in to_be_adjusted:
            # get the nation for the NC
            #country = tbd.country
            # get the year in which this race is
            #year = tbd.year
            # count the number of riders sold in given year
            ridercount = VirtualTeam.objects.filter(editie=tbd.editie).filter(rider__nationality__icontains=tbd.country.upper()).count()
            # NC1
            #print(tbd.country, tbd.category, tbd.editie, ridercount)
            if ridercount > 9:
                # set category to NC1 if 10 or more are sold and it is a NC
                # copy points from 1.WT3 to NC 1
                if tbd.category.id < 19:
                    tbd.category = Category.objects.get(id=14)
                else:
                    # NCT1, set category to NCT1 if it's a NCT, time-trial
                    tbd.category = Category.objects.get(id=19)
            elif ridercount > 4:
                # NC2
                if tbd.category.id < 19:
                    tbd.category = Category.objects.get(id=15)
                    #tbd.category_id = 15
                else:
                    # NCT2
                    tbd.category = Category.objects.get(id=20)
            else:
                # all others, even if no riders are sold
                # use NC3 for this id = 16
                if tbd.category.id < 19:
                    tbd.category = Category.objects.get(id=16)
                else:
                    # NCT3
                    tbd.category = Category.objects.get(id=21)
            tbd.save()
            print(tbd.country, tbd.category, tbd.editie, ridercount)

