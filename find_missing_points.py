from results.models import CalculatedPoints, Rider
from auction.models import VirtualTeam

"""
I want to know for which riders there is a difference between CalculatedPoints and
the 'official' points. Let's start by looking up the official values
"""
difference = []
for year in [2022, 2021, 2020, 2019]: 

    sold_riders = VirtualTeam.objects.filter(editie=year)
    #print(sold_riders)

    #earnings = CalculatedPoints.objects.filter(editie=year)

    for s in sold_riders:
        calc = CalculatedPoints.objects.get(editie=year, rider=s.rider)
        #print(s.rider, s.punten, s.jpp, calc.points, calc.jpp)

        if s.punten != calc.points:
            #print(f"Verschil voor {s.rider} ({s.rider.id}) in {year}")
            difference.append([year, s.rider.name, s.rider.id, float(s.punten), float(calc.points), s.jpp, calc.jpp])

for d in difference:
    print(d)


