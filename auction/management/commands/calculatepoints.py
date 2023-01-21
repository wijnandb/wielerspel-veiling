from django.core.management.base import BaseCommand, CommandError

from auction.models import VirtualTeam, TeamCaptain 
from results.models import Race, Rider, Uitslag, RacePoints, CalculatedPoints

class Command(BaseCommand):
    help = 'Calculate the points a rider has accumulated and store it somewhere'

    def handle(self, *args, **options):
        """
        To keep the "official" nformation, store the calculated points in a different model or field.
        I want to be able to calculate all points for all riders, not just for sold ones, so
        let's create a different model to do so.
        Model CalculatedPoints, that has rider, year, points and JPP
        WIP: if a rider wins a big Tour, deduct the points for wearing the leaders jersey
        WIP: if a season starts later, do not calculate the first races of the season
        Categories whose points are dependent on sold riders per country/continent in that year:
        NC1=14
        NC2=
        NC3=
        """
        #for year in range(2022, 2018, -1):
        year = 2021
        
        riders = Rider.objects.filter()
        # this is a lot, maybe only take the ones that get a result
        print(riders.count())
        for rider in riders:
            points = 0
            jpp = 0
            # look for rider in results, then update 

            results = Uitslag.objects.filter(rider=rider).filter(race__startdate__year=year)
            #print(len(results))

        # the RacePoints can be seen as a list, I can even filter that list, only remaining
        # the items with points > 0
            for result in results:
                try:
                    add_up = RacePoints.objects.get(ranking=result.rank, category__race=result.race)
                    points = points + add_up.points
                    jpp = jpp + add_up.jpp
                except:
                    continue

            try:
                update_points = CalculatedPoints.objects.get(rider=rider, editie=year)
                print(f"Found {rider}, points: {points}, jpp: {jpp}")
                update_points.points=points
                update_points.jpp=jpp
                update_points.save()
            except:
                CalculatedPoints(rider=rider, editie=year, points=points, jpp=jpp)
                print(f"Created a new record for {rider}")
