def main():
    # WIP: maybe only check for the next month or on a certain day
    #scrape_calendar(2023)
    # WIP: create a results page per month
    #get_results()
    # create_html_file('/home/wijnandb/sites/heroku/wielerspel/scraping/csv/2023/ploegen.csv', 'scraping/HTML/ploegen.html')
    add_points_to_results()
    #add_points_to_riders()
    #add_points_to_teamcaptains()
    #calculate_ranking_wielerspel()
    # teamcaptains = get_teamcaptains(sold_riders)
    # table = get_points_per_teamcaptain(teamcaptains)
    # print(table)
    add_tc()
    


import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime


with open('/home/wijnandb/sites/heroku/wielerspel/scraping/csv/2023/ploegen.csv', newline='') as f:
        readriders = csv.reader(f)
        sold_riders = list(readriders)

with open('/home/wijnandb/sites/heroku/wielerspel/scraping/csv/2023/results_with_points.csv', newline='') as f:
        readresults = csv.reader(f)
        results = list(readresults)

# with open('/home/wijnandb/sites/heroku/wielerspel/scraping/csv/2023/riders_with_points.csv', newline='') as f:
#         riderswithpoints = csv.reader(f)
#         riderspoints = list(riderswithpoints)


categories = {
    '1.1': 1,
    '2.1': 2,
    '1.PS': 3,
    '2.PS': 4,
    '2.WT1': 5,
    '2.WT2': 6,
    '2.WT3': 7,
    '1.WT1': 8,
    '1.WT2': 9,
    '1.WT3': 10,
    'GT1': 11,
    'GT2': 12,
    'WCRR': 13,
    'NC1': 14,
    'NC2': 15,
    'NC3': 16,
    'NC4': 17,
    'NC5': 18,
    'NCT1': 19,
    'NCT2': 20,
    'NCT3': 21,
    'NCT4': 22,
    'NCT5': 23,
    'CC1': 24,
    'CC2': 25,
    'CCT1': 26,
    'CCT2': 27,
    '2.1s': 28,
    '2.PSs': 29,
    '2.WT1s': 30,
    '2.WT2s': 31,
    '2.WT3s': 32,
    'GT1s': 33,
    'GT2s': 34,
    'GT1r': 35,
    'GT2r': 36,
    '2.WT1r': 37,
    '2.WT2r': 38,
    '2.WT3r': 39,
    '1.HC': 40,
    '2.HC': 41,
    '2.HCs':42,
    'WCTT':43,
}
has_stages = [2,4,5,6,7,11,12,41]

def calculate_ranking_wielerspel():
    """
    Here I want to loop through all riders and look up the results, 
    add up the point earned and add that to the rider.
    Then I want to loop through the riders of a Teamcaptain and add up the points of those riders.

    Finaly I want to order the teamcaptains by points and JPP and publish a ranking.
    
    """
    pass

def add_tc():
    import csv
    with open('/home/wijnandb/sites/heroku/wielerspel/scraping/csv/2023/ploegen.csv', newline='') as f:
        readriders = csv.reader(f)
        sold_riders = list(readriders)

    # read csv file results_with_points
    with open('/home/wijnandb/sites/heroku/wielerspel/scraping/csv/2023/results_with_points.csv', newline='') as f:
        readresults = csv.reader(f)
        results = list(readresults)

    updated_results = []
    # loop over both files
    for result in results:
        result.append("niet verkocht")
        print(result)
        for rider in sold_riders[1:]:
            # if rider == rider
            if result[3] == rider[0]:
                print(f"{result[3]} == {rider[0]}")
                # add tc to result
                result[7]=rider[3]
        print(result)
        updated_results.append([int(result[0]),result[1],int(result[2]),int(result[3]),result[4],float(result[5]),int(result[6]),result[7]])
    
    # create new csv file results_points_teamcaptain.csv
    with open('scraping/csv/2023/results_points_teamcaptain.csv', 'w') as f:
        write = csv.writer(f)
        write.writerows(updated_results)


def add_points_to_riders():
    #print(results)
    if check_integrity_soldriders(sold_riders):
        with open('scraping/csv/2023/results_with_points.csv', 'r') as f:
            pointresults = csv.reader(f)
            results_with_points = list(pointresults)
        
        calculated = []
        # You want to do it differently. First, you calculate the points per rider and update those 
        # points and JPP  
        for rider in sold_riders[1:]:
            #print(rider)
            points = 0
            JPP = 0
            for result in results_with_points:
                # print(result)
                if rider[0] == result[3]:
                    print(f"{rider[0]} == {result[3]}")
                    print(f"Points: {points}, JPP: {JPP}")
                    points += float(result[5])
                    JPP += int(result[6])
                    print(f"Points: {points}, JPP: {JPP}")
                # else:
                #     print(f"{rider[0]} != {result[3]}")
            rider[8] = points
            rider[9] = JPP
            calculated.append([int(rider[0]),rider[1],rider[2],rider[3],int(rider[4]),rider[5],rider[6],int(rider[7]),float(rider[8]),int(rider[9])])
            if rider[8] > 0:
                print(calculated[-1])

        with open('scraping/csv/2023/riders_with_points.csv', 'w') as f:
            write = csv.writer(f)
            write.writerows(calculated)
        
        """
        I can call the next function here, passing in the results
        """
        
        # teamcaptains = get_teamcaptains(sold_riders)
        # table = get_points_per_teamcaptain(teamcaptains)
        # # print(calculated)
        # print(table)

    
        
# def get_points_per_teamcaptain(teamcaptains):
#     """
#     Add earned points per rider to the list with riders.
#     Loop through the riders per teamcaptain and add up all points
#     """ 
#     stand = []
#     for tc in teamcaptains:
#         print(f"{tc}\n")
#         points = 0
#         jpp = 0
#         riders = get_riders_per_teamcaptain(riderswithpoints, tc)
#         for rider in riders:
#             for result in riderspoints:
#                 if rider[0] == result[3]:
#                     print(f"{rider[0]} == {result[3]} ")
#                     points += int(result[8])
#                     jpp += int(result[9])
#                 #else:
#                     #print(f"{rider[0]} != {result[3]} ")
#         stand.append([tc, points, jpp])
#     return stand


def get_riders_per_teamcaptain(sold_riders, teamcaptain):
    team = []
    for rider in sold_riders:
        if rider[3] == teamcaptain:
            team.append(rider)
            #print(rider)
    return team

    
def get_teamcaptains(sold_riders):
    teamcaptains = []
    for sr in sold_riders[1:]:
        if sr[3] not in teamcaptains:
            teamcaptains.append(sr[3])
    return teamcaptains


def check_integrity_soldriders(sold_riders):
    teamcaptains = []
    totalspent = 0 
    for sr in sold_riders[1:]:
        if sr[3] not in teamcaptains:
            teamcaptains.append(sr[3])
        totalspent += int(sr[4])

    assert len(teamcaptains) == 14
    assert totalspent == 1400

    #stats = [["teamcaptain", "spent", "# riders"]]
    for tc in teamcaptains:
        spent = 0
        riders = 0
        for sr in sold_riders[1:]:
            if tc == sr[3]:
                spent += int(sr[4])
                riders += 1
                #get_results_rider(sr[0])
        #stats.append([tc, spent, riders])
        assert spent == 100
        assert riders >= 10
        assert riders <= 30
    return True



def get_id_from_sold_riders():
    """
    Finding the id's from CQranking by comparing the names of the riders.
    Please note: apostrophe doesn't get found, i.e. O'CONNOR
    Compare two files, the list of sold riders in Wielerspel and the file from CQranking or a slightly 
    altered version of it (export from Django admin, wielerspel site) 
    """
    tweenamen = 0
    drienamen = 0 
    viernamen = 0
    ploegen = [['id','renner','rider','ploegleider','kosten','team','nationality','age','punten','JPP'],
                [23763,"O'CONNOR Ben","O'CONNOR Ben","Harry",7,"ACT","AUS",0,0],]
    with open('/home/wijnandb/sites/heroku/wielerspel/scraping/csv/2023/verkochte_renners_2023.csv', newline='') as f:
        reader = csv.reader(f)
        sold_riders = list(reader)
    
    with open('/home/wijnandb/sites/heroku/wielerspel/scraping/csv/2023/Rider-2023-01-20.csv', newline='') as f:
        reader = csv.reader(f)
        riderids = list(reader)
    
    for renner in sold_riders[1:]:
        names = renner[0].split(" ")
        #print(len(names))
        try:
            for rider in riderids:
                if len(names)>3:
                    if (names[0] in rider[5]) and (names[1] in rider[5]) and (names[2] in rider[5]) and (names[3] in rider[5]):
                        viernamen += 1
                        ploegen.append([int(rider[0]),renner[0],rider[5],renner[1],int(renner[2]),rider[6],rider[7],int(rider[8]),int(renner[3]),int(renner[4])])
                elif len(names)==3:
                    if (names[0] in rider[5]) and (names[1] in rider[5]) and (names[2] in rider[5]):
                        drienamen += 1
                        ploegen.append([int(rider[0]),renner[0],rider[5],renner[1],int(renner[2]),rider[6],rider[7],int(rider[8]),int(renner[3]),int(renner[4])])
                elif len(names)==2:
                    if (names[0] in rider[5]) and (names[1] in rider[5]):
                        tweenamen += 1
                        ploegen.append([int(rider[0]),renner[0],rider[5],renner[1],int(renner[2]),rider[6],rider[7],int(rider[8]),int(renner[3]),int(renner[4])])
                else:
                    print(f"Renner {names} met naamlengte {len(names)} niet gevonden.\nKorter dan 2 of langer dan 4.")
                    
              
        except:
            print(f"{renner[0]} niet gevonden")
        
    with open('ploegen-met-ids.csv', 'w') as f:
        
        # using csv.writer method from CSV package
        write = csv.writer(f)
        
        #write.writerow(fields)
        write.writerows(ploegen)
        
        print("output ploegen met ids geschreven")
        print(f"dubbele achternaam: {tweenamen}")
        print(f"3x achternaam: {drienamen}")
        print(f"4x achternaam: {viernamen}")
        print(f"totaal = {tweenamen+drienamen+viernamen}")

    
def create_html_file(input, output):
    import csv
    with open(input, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    fileout = open(output, "w")

    table = "<html>\n\t<head>\n\t\t<title>Stand Wielerspel 2023</title>\n\t</head>\n\t<body>\n\t\t<table>\n"

    # Create the table's column headers
    header = data[0]
    table += "\t\t\t<tr>\n"
    for column in header:
        table += "\t\t\t\t<th>{0}</th>\n".format(column.strip())
    table += "\t\t\t</tr>\n"

    # Create the table's row data
    for row in data[1:]:
        table += "\t\t\t<tr>\n"
        for column in row:
            table += "\t\t\t\t<td>{0}</td>\n".format(column.strip())
        table += "\t\t\t</tr>\n"

    table += "\t\t</table>\n\t</body>\n</html>"

    fileout.writelines(table)
    fileout.close()

    print("file gegenereerd")


def get_results_rider(rider, year=2023):
    """
    If I am getting the results per rider, I might as well create a separate file per rider and create 
    an HTML page for it as well
    """
    results = []
    base_result_url = f"https://cqranking.com/men/asp/gen/rider_palm.asp?riderid={rider}&year={year}&all=0&current=0"
    r = requests.get(base_result_url)
    soup = BeautifulSoup(r.text, "html.parser")
    try:
        result = soup.find_all("th", ["tabheaderLTB", "tabrow2"])
        result_tr = result[1].parent
        result_table = result_tr.parent

        row_tags = result_table.find_all('tr')[3:] # skipping the header rows
        for row_tag in row_tags:
            try:
                tds = row_tag.find_all('td')
                startdate = tds[1].text#+"/" + str(year)
                print(startdate)
                racecat = tds[3].text
                print(racecat)
                country = tds[5].img['title']
                print(country)
                rank = int(tds[7].text.strip())
                racename = tds[9].text
                cqraceid = int(tds[9].a['href'].split("=")[1])
                print(startdate,racecat,country,rank,racename, cqraceid)
                results.append([startdate,racecat,country,rank,racename, cqraceid])
            except:
                pass
        # Write the results to a CSV file
        with open('scraping/csv/results_per_rider.csv', 'w') as f:
            write = csv.writer(f)
            write.writerows(results)
    except:
        print(f"No results for {rider}")


def scrape_calendar(year=2023):
    # get current month and scrape that plus one
    # or check for the day and scrape on the 28th of the month
    races = []
    stageraces = []
    startURL = 'https://cqranking.com/men/asp/gen/RaceCal.asp?year='
    for i in range(1,2):
        try:
            b = startURL+str(year)+"&month="+str(i)
            r =requests.get(b)
            soup = BeautifulSoup(r.text, "html.parser")
            first_result = soup.find("td", ["tabrow1simple","tabrow2simple"])
            result_tr = first_result.parent
            result_table = result_tr.parent
            for tr in result_table.find_all('tr')[1:]:
                tds = tr.find_all('td')
                """
                Make a distinction between one day races and multi-day races.
                Start with finding out whether this is a one-day or multiday race.
                """
                category = tds[7].text.strip()
                racename = tds[11].text
                startdate = tds[3].text
                country = tds[9].img['title']
                if category in ['2.1','2.PS','2.WT1','2.WT2','2.WT3','GT1','GT2',]:
                    #get_stages_multidayrace(racename, int(tds[13].a['href'].split("=")[1]), year, category, country)
                    stageraces.append([racename, int(tds[13].a['href'].split("=")[1]),year,category, country])
                else: 
                    cqraceid = int(tds[11].a['href'].split("=")[1])
                    #print(cqraceid, racename, startdate, category, country)
                    races.append([cqraceid, racename, startdate, category, country])

        except:
            pass
            # Write the results to a CSV file
    with open('scraping/csv/2023/racecalendar.csv', 'w') as f:
        write = csv.writer(f)
        write.writerows(races)
    for sr in stageraces:
        get_stages_multidayrace(sr[0], sr[1],sr[2],sr[3],sr[4])


def get_stages_multidayrace(racename, race_id, year, category, country):
    """
    - visit race page
    - get id's for stages
    - filter for different rankings
    - store stage as race with same category + "s"

    """
    stages = []
    base_result_url = "https://cqranking.com/men/asp/gen/tour.asp?tourid="
    b = base_result_url + str(race_id)
    r = requests.get(b)
    soup = BeautifulSoup(r.text, "html.parser")
    first_result = soup.find("td", ["tabrow1", "tabrow2"])
    result_tr = first_result.parent
    result_table = result_tr.parent


    row_tags = result_table.find_all('tr')[1:] # skipping the header row

    for row_tag in row_tags:
        try:
            tds = row_tag.find_all('td')
            startdate = tds[1].text +"/" + str(year)
            fullname = racename +" "+ tds[7].text
            #print(fullname, category)
            cqraceid = int(tds[7].a['href'].split("=")[1])
            #print(f"Raceid = {cqraceid}")
            # Now add race to races:
            if "point" in tds[7].text[0:5] or "mount" in tds[7].text:
                lookupcat = str(category)+"r" 
            elif "General" not in tds[7].text[0:10]:
                lookupcat = str(category)+"s"
            if lookupcat:               

            #print(cqraceid, racename, startdate,lookupcat, country)
                stages.append([cqraceid, fullname, startdate,lookupcat, country])
            # try:
            #     stagewinner = tds[11].a['href'].split("=")[1]
            # except:
            #     pass
            
            # if stagewinner:
            #     # I could enter the result here, write it to full-results
            #     # Can be done for all 
            #     pass
        
            #print(stages)

        except:
            continue

    with open('scraping/csv/2023/racecalendar.csv', 'a') as f:
        write = csv.writer(f)
        write.writerows(stages)
        print("written")


def get_results():
    # load csv with calendar races
    with open('/home/wijnandb/sites/heroku/wielerspel/scraping/csv/2023/racecalendar.csv', newline='') as f:
        reader = csv.reader(f)
        races = list(reader)
    present = datetime.now()
    # iterate over races in calendar
    for race in races:
        #  check if race is over
        past = datetime.strptime(race[2], "%d/%m/%Y")
        if past.date() == present.date():
            print(f"This race has finished! {race[1]}")
            # check if we already have the results
            get_results_per_race(race[0], race[1], race[3])
        else:
            print(f"NOT FINISHED YET! {race[1]}")


def get_results_per_race(race_id, race_name, category):
    """
    Look at the calendar, see which races there are, check them for results.
    I can visit a URL and get the results.
    I could also mark a race as 'processed', so I won't visit again and again.
    Will do or think about that later.

    How am I going to store results?
    I guess I need the full details of a race, plus the name and id of the rider, plus the name of the 
    teamcaptain, plus the number of points and JPP.
    It all depends on how I will be able to process points and JPP.
    Looping over the teams per teamcaptain 
    Top 20 TdF klassement, top 15 klassement Giro/Vuelta
    Create an array with catgeories and corresponding number of results to be taken in

    WIP:
    Appending results can lead to double results.
    Writing results means getting all results every day again, which is unnecessary
    (and is causing another problem, where I only have the rsults of the last race...)
    """
    results = []
    if category[-1] == "s":
        # stage or mountains/points, only get winner and leader
        rankings = 2 
    elif category in ['1.1', '2.1']:
        # only get top 3
        rankings = 3
    elif category in ['GT1', 'GT2']:
        # grandtour, get top 15 or top 20
        rankings = 20
    else:
        # all others have top 10 for JPP
        rankings = 10
    
    base_result_url = "https://cqranking.com/men/asp/gen/race.asp?raceid="
    b = base_result_url + str(race_id)
    r = requests.get(b)
    soup = BeautifulSoup(r.text, "html.parser")
    first_result = soup.find("td", ["tabrow1", "tabrow2"])
    result_tr = first_result.parent
    result_table = result_tr.parent
 
    row_tags = result_table.find_all('tr')[1:rankings+1] # skipping the header row, top x only

    for row_tag in row_tags:
        points = 0
        JPP = 0
        try:
            tds = row_tag.find_all('td')
            if tds[1].text == 'leader':
                # print("###########################")
                # print("We have found the leader. Only need this for GT1 and GT2")
                # print("###########################")
                # Leader of the race gets position 0 (has to be integer)
                # in pages we change this to "Leader"
                rank = 0
                if (category=='GT1s') or (category=='GT2s'):
                    points = 1
            else:
                rank = tds[1].text.split(".")[0]
            #print(int(rank))
            rider = tds[5].a['href'].split("=")[1]
            print(f"Resultaat: {rank}, {race_name}, {race_id}, {rider}, {category}, {points}, {JPP},")
            results.append([rank, race_name, race_id, rider, category, points, JPP])
        except:
            continue
    
    # store results in CSV
    # WIP: check if a result already exists before writing
    # check for double entries with an assert
    # combination of race and rank can occur only once 
    with open('scraping/csv/2023/results.csv', 'a') as f:
        write = csv.writer(f)
        write.writerows(results)
    

def add_points_to_results():
    # get results from csv
    with open('/home/wijnandb/sites/heroku/wielerspel/scraping/csv/2023/results.csv', newline='') as f:
        reader = csv.reader(f)
        results = list(reader)
    if test_results_integrity(results):
        # haal point binnen
        with open('/home/wijnandb/sites/heroku/wielerspel/scraping/csv/2023/points.csv', newline='') as f:
            reader = csv.reader(f)
            points = list(reader)
        # make sure there are no duplicate results
        results_with_points = []
        # loop over results
        for result in results:
            # update points for results
            for point in points:
                # same category and same ranking
                if (result[4]==point[0]) and (result[0]==point[1]):
                    print(f"True for {result[1]}, {result[4]} and {result[0]}")
                    # award points
                    result[5]=float(point[2])
                    # award JPP
                    result[6]=int(point[3])
                    results_with_points.append([int(result[0]),result[1],int(result[2]),int(result[3]),result[4],float(result[5]),int(result[6])])
                    print([int(result[0]),result[1],int(result[2]),int(result[3]),result[4],int(result[5]),int(result[6])])
        with open('scraping/csv/2023/results_with_points.csv', 'w') as f:
            write = csv.writer(f)
            write.writerows(results_with_points)
        
        add_points_to_riders()

    else:
        print("Results are compromised (add_points_to_results, line 525")

    
            

def test_results_integrity(results):
    """
    I want to make sure that there is only one rider per position per race
    """
    processed = []
    # loop over results
    for result in results:
        if [result[2],result[0]] in processed:
            return False
        else:
            processed.append([result[2],result[0]])
    return True  
    
    
if __name__ == "__main__":
    main()
