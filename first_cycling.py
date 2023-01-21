import requests
from bs4 import BeautifulSoup
import psycopg2
import pandas as pd
import urllib.request
import csv
from datetime import datetime
from results.models import Rider, Race, Uitslag
import unicodedata

def scrape_results():
    """
    We want to find the results for Youth, Points and Mountain rankings for the big Tours
    (TdF, Giro, Vuelta)
    url looks like: https://firstcycling.com/race.php?r=23&y=2022
    r is raceID, Vuelta = 23 TdF = 17 and Giro = 13
    year can als be changed.
    All rankings are loaded at once.
    The results are in different div's, with id's 
    Separate pages per stage: 
    https://firstcycling.com/race.php?r=23&y=2022&e=01 (e=1 works as well)

    It is possible that a ranking is not there, for instance youth in Vuelta 2018

    WIP: add endwinner for Youth ranking
    """
    races= [["Giro", 13, "Giro d'Italia Stage "],["Vuelta", 23, "Vuelta a España Stage "], ["Tour de France", 17, "Tour de France Stage "], ]
    errors = []
    results=[]
    #year = 2022 # 
    years = range(2021, 2019, -1)
    for year in years:
        for race in races:
            typeranking = ["youth", "point", "mountain"]
            for typerank in typeranking:
                winner = ""
                print(F"Getting results for { year } { race[0] }")
                for stage in range(21, 0, -1):
                    base_result_url = "https://firstcycling.com/race.php?r="
                    b = base_result_url + str(race[1]) + "&y=" + str(year) +"&e=" +str(stage)
                    #print(f"Opening page.... {b}")
                    r = requests.get(b)
                    soup = BeautifulSoup(r.text, "html.parser")
                    racename = race[2] + str(stage)
                    #print(racename)
                    try:
                        resultsdiv = soup.find("div", {"id":typerank})
                        body = resultsdiv.find("tbody")
                        rows = body.find_all("tr")
                        for i in range(len(rows)):
                            #print(f"Check row {i}")
                            first_row = rows[i]
                            tds = first_row.find_all("td")
                            position = tds[0].text.strip()
                            if int(position) == 1:
                                leader = tds[3].text.strip()
                                #if stage == 21:
                                    #winner = tds[3].text.strip()
                                #if leader == winner:
                                    #print(f"{leader} is also {winner}, skip.")
                                    #break
                                #else:
                                cqrider = find_rider(leader)
                                #print(cqrider)
                                cqrace  = find_race(racename, year)
                                #print(cqrace)
                                add_result(cqrider, cqrace, typerank)
                                results.append([cqrider, cqrace, typerank])
                                #print(year, race[0], year, stage, leader, typerank)
                                #results.append([position, leader, cqrider.id, cqrider.name, year, race[0], stage, typerank])
                                #print(f"Now break after row { i }")
                                break
                    except:
                        errors.append([position, leader, year, race[0], stage, typerank])
                        continue

    print("Found the following errors:")
    for result in errors:
        print(f"{ result }")
    
    print("can be added:")
    for result in results:
        print(result)



def get_points_leadersjersey(year=2022, race=2, stages=21, jersey="youth"):
    races= [["Giro", 13, "Giro d'Italia Stage"],["Vuelta", 23, "Vuelta a España Stage"], ["Tour de France", 17, "Tour de France Stage"], ]
    errors = []
    results=[]
    #print(F"Getting results for { year } { races[race][0] }")
    for stage in range(1, stages+1):
        base_result_url = "https://firstcycling.com/race.php?r="
        b = base_result_url + str(races[race][1]) + "&y=" + str(year) +"&e=" +str(stage)
        #print(f"Opening page.... {b}")
        r = requests.get(b)
        soup = BeautifulSoup(r.text, "html.parser")
        racename = races[race][2] +" " + str(stage)
        #print(racename)
        try:
            resultsdiv = soup.find("div", {"id":jersey})
            body = resultsdiv.find("tbody")
            rows = body.find_all("tr")
            for i in range(len(rows)):
                #print(f"Check row {i}")
                first_row = rows[i]
                tds = first_row.find_all("td")
                position = tds[0].text.strip()
                if int(position) == 1:
                    leader = tds[3].text.strip()
                    cqrider = find_rider(leader)
                    #print(cqrider)
                    cqrace  = find_race(racename, year)
                    #print(cqrace)
                    add_result(cqrider, cqrace, jersey)
                    results.append([cqrider.id, cqrace.id, jersey])
                    #print(year, race[0], year, stage, leader, typerank)
                    #results.append([position, leader, cqrider.id, cqrider.name, year, race[0], stage, typerank])
                    #print(f"Now break after row { i }")
                    break
        except:
            errors.append([year, races[race][0], stage, jersey])
            continue

    print("Found the following errors:")
    for result in errors:
        print(f"{ result }")

    print("can be added:")
    for result in results:
        print(result)



def find_jerseywinner(year=2022):
    print(f"Finding jerseywinners Grand Tours for the year {year}")
    # Who won the diferent jerseys?
    # which races were GT1 en GT2?
    # GT1 categorie: 11 GT2 category: 12
    # For mountain and points, categories are 35 (GT1r, Tour de France) and 36 (GT2r, Vuelta, Giro)
    # first, the winner of the Grand Tour:
    winner = Uitslag.objects.filter(race__startdate__year=year).filter(race__category__in={11, 12}).filter(rank=1)
    print(winner)
    for rw in winner:
        # the wearer of the leadersjersey gets rank=0 in the stageresults
        #print(rw.race, rw.rider, rw.race.editie, rw.race.country, 1)
        remove_points(rw.race, rw.rider, 0, year)
    
    mountainwinner = Uitslag.objects.filter(race__startdate__year=year).filter(race__category__in={35,36}).filter(rank=1).filter(race__name__icontains="Mountain")
    for rw in mountainwinner:
        print("Finding stages where Mountain-winner wore the mountain jersey")
        remove_points(rw.race, rw.rider, -2, year)
    
    pointswinner = Uitslag.objects.filter(race__startdate__year=year).filter(race__category__in={35,36}).filter(rank=1).filter(race__name__icontains="Point")
    for rw in pointswinner:
        print("Finding stages where points-winner wore the points jersey")
        remove_points(rw.race, rw.rider, -3, year)

    youthwinner = Uitslag.objects.filter(race__startdate__year=year).filter(race__category__in={11, 12}).filter(rank=-1)
    for rw in youthwinner:
        print("Finding stages where Youth-winner wore the Youth jersey")
        remove_points(rw.race, rw.rider, -1, year)


def find_alternative_rankings():
    """
    Find for which stages we have jersey wearers for Leader, Youth, Mountain and Points
    """
    pass


def remove_points(race, rider, rank, year):
    """
    Find the stages where the final winner of a jersey is listed as the wearer.
    Remove those, for he cvan not get points for wearing a jersey if he also won it
    """
    toberemoved= Uitslag.objects.filter(rider=rider, rank=rank, race__country=race.country, race__category__in={33, 34}, race__startdate__year=year)
    for tbr in toberemoved:
        print(f"To be removed: {tbr.race}, {tbr.rider}, {tbr.rank}")
        tbr.delete()


def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')


def find_rider(rider):
    """
    I want to look up the rider in the Rider model, by comparing the name.
    If I find the rider, I can also add that rider to a table that connects FirstCycling id's 
    to CQranking id's.

    """
    try:
        CQrider = Rider.objects.get(name__icontains=rider)
        return CQrider
    except:
        try:
           CQrider = Rider.objects.get(name__icontains=rider.split(" ")[0]+" ")
           return CQrider
        except:
            return(f"Helaas {rider} niet gevonden")


def find_race(race, year):
    """
    I look up the stage after which someone wore a jersey (youth, mountains, points)
    I then add a record, where 
    -1 is the ranking for the Youth jersey,
    -2 is the ranking for the Mountains jersey and
    -3 is the ranking for the Points jersey.
    Final winners of a jersey are excluded, so I don't have to c ompensate for excess earnings.

    In the page I could even use an array to display the correct ranking description:
    description = ["Leader", "Points", "Mountains", "Youth"]
    In this array, 
    0 = leader
    -1 = Youth
    -2 = Mountains
    -3 = Points
    """
    try:
        # instead of returning the Race object, I can create a new object
        # Not doing that, adding the result to existing stages
        return Race.objects.get(name__icontains=race, editie=year)
    except:
        return(f"Helaas {race} niet gevonden")

def add_result(cqrider, cqrace, typerank):
    """
    Add the jersey wearers to the stageresult.
    Check if an entry already exists, so you can update it. Otherwise, create a new record.
    Rank for Youth = -1
    Mountains = -2
    Points = -3
    WIP: make it possible to update if I happen to have inserted the wrong result
    """
    print(cqrider, cqrace, typerank)
    if typerank == 'youth':
        rank = -1
    elif typerank == 'mountain':
        rank = -2
    elif typerank == 'point':
        rank = -3
    else:
        print(f"Didn't find {typerank}")

    if rank:
        try:
            result = Uitslag.objects.get(race=cqrace, rank=rank)
            result.rider =cqrider
            result.save()
            print(f"Updated result for {cqrace.name}, ({cqrace.id}) rank {rank} for {cqrider.name} ({cqrider.id})")
        except:
            Uitslag.objects.create(race=cqrace, rank=rank, rider=cqrider)
            print(f"Created new result for {cqrace.name}, ({cqrace.id}) rank {rank} for {cqrider.name} ({cqrider.id})")


#scrape_results()

#Uitslag.objects.create(race_id=40460, rank=-1, rider_id=28377)
#Uitslag.objects.create(race_id=40010, rank=-1, rider_id=26526)
#Uitslag.objects.filter(race__editie=2022, race__category=34, rank=0, rider_id=28377).delete()

#print(find_rider('CORT Magnus').id)
#find_jerseywinner(2021)

def create_new_results():
    results=[
    [18610, 38359, -3],
    [12193,38359,-2],
    [18610,38360,-3],
    [21971,38360,-2],
    [12843,38367,-2],
    [12843,38368,-2],
    [12843,38369,-2],
    [12843,38370,-2],
    [12843,38371,-2],
    [28452,38431,-1],
    [25653, 38431, -2],
    [20719, 38431, -3],
    [28452, 38432, -1],
    [25653, 38432, -2],
    [26392, 38432, -3],
    ]

    for r in results:
        try:
            tbu = Uitslag.objects.get(race_id=r[1], rank=r[2])
            print(tbu.rider, tbu.race, tbu.rank)
        #tbu.rider_id = r[0]
        #tbu.save()
        except:
            new = Uitslag.objects.create(race_id=r[1], rider_id=r[0], rank=r[2])
            print(f"Nieuw aangemaakt: {new.rider}, {new.race}, {new.rank}")
        # try:
        #     tobe_inserted= Uitslag.objects.get(race_id=r[1], rank=r[2])
        #     tobe_inserted(rider_id=r[0])
        #     tobe_inserted.save()
        #     print(f"Inserted: {r[0]}, {r[1]}, {r[2]}")
        #     print(tobe_inserted.rider, tobe_inserted.race, tobe_inserted.rank)
        # except:
        #     new = Uitslag.objects.create(race_id=r[1], rider_id=r[0], rank=r[2])
        #     print(f"Nieuw aangemaakt: {new.rider}, {new.race}, {new.rank}")
    

# Uitslag.objects.create(race_id=38432, rank=-3, rider_id=26392)

#Uitslag.objects.get(race_id=40439, rank=-3, rider_id=13362).delete()
# for year in range(2020, 2022):
#     for race in range(3):
#         for jersey in ["youth", "mountain", "point"]:
#             print(f"{jersey} in race {race} for the year {year}")
#             get_points_leadersjersey(year, race, 21, jersey)

for year in [2022, 2021, 2020, 2019]:
    get_points_leadersjersey(year, 0)
    get_points_leadersjersey(year, 1)
    get_points_leadersjersey(year, 2)
    find_jerseywinner(year)