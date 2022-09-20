# this script is to scrape the CQranking calendar and results
# we store the results in the Race-table in 
# /home/wijnandb/sites/heroku/wielerspel/results/models.py
# challenges:
# - can't store results for unknown races
# - can't store results for unknown riders
# - teamresults have no corresponding riderid, so have to be skipped
# Should I scrape data, store it in either a set of a CSV, then clean it?
# Should I compare the results lists with the races and riders list, to check if they are in it?
# if renner in renners:
#   update renner
# else:
#   insert renner
# Same for races 
# Probably have to recreate 
# import libraries
import requests
from bs4 import BeautifulSoup
import psycopg2
import pandas as pd
import urllib.request
import csv
from datetime import datetime

# load data for current season

# with open('/home/wijnandb/sites/heroku/wielerspel/scraping/csv/2022/veilingdata/ploegen.csv', newline='') as f:
#     reader = csv.reader(f)
#     ploegen = list(reader)

# with open('/home/wijnandb/sites/heroku/wielerspel/scraping/csv/2022/veilingdata/ploegleiders.csv', newline='') as f:
#     reader = csv.reader(f)
#     ploegleiders = dict(reader)

# res =[i + [ploegleiders[i[2]], i[2]] for i in ploegen[1:]]

# for r in res:
#     print(r)


# define starturl
# year is now hardcoded, can be changed
startURL = 'https://cqranking.com/men/asp/gen/RaceCal.asp?year='

def bulkInsert(records, type):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="localpostgres",
                                      port="5432",
                                      database="wielerspel")
        cursor = connection.cursor()
#         this is query for races from calendar
        if type==1:
            #print("insert races")
            sql_insert_query = """INSERT into results_race(id, cqraceid, name, startdate, enddate, category_id, country, editie) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
# this is query for results
        elif type==2:
            #print("insert results")
            sql_insert_query = """INSERT into results_uitslag(rank, race_id, rider_id) VALUES (%s, %s, %s)"""
        elif type==3:
            sql_insert_query = """ INSERT into results_rider(id, cqriderid, ucicode, name, nationality, sold)
                            VALUES (%s, %s, %s, %s, %s, %s) """
        # executemany() to insert multiple rows rows
        else:
            #print("failed to find correct query")
            pass
        cursor.execute(sql_insert_query, records,)
        connection.commit()
        #print(cursor.rowcount, "Record inserted successfully into table")

    except (Exception, psycopg2.Error) as error:
        #print("Failed inserting record into table {}".format(error))
        pass

    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is closed")


# reviewing the code of the page tells us the table to scrape is among a lot
# of other tables. Ours is recognizable by the td class="tabrow1simple"
# we want to find the first, then go to the parent tr, find all the tr's
# loop over each tr and get the values from the td's
# 
# we want all months, except december
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
races = []
results = []
riders = []
def scrape_calendar(year):
    year = str(year)   
    # WIP: limit time, only scrape current month
    for i in range(1,13):
    #for i in range(7,8):
        try:
            b = startURL+str(year)+"&month="+str(i)
            #print(b)
            r = requests.get(b)
            soup = BeautifulSoup(r.text, "html.parser")
            first_result = soup.find("td", ["tabrow1simple","tabrow2simple"])
            #print(first_result)
            # now get the parent tr
            result_tr = first_result.parent
            #print(result_tr)
            # and the parent table
            result_table = result_tr.parent
            #print(result_table)
            # now we found the right table, we want all tr's within
            for tr in result_table.find_all('tr')[1:]:
                # we skip the header row, hence [1:]
                tds = tr.find_all('td')
                #print (tds[3].text, tds[5].text, tds[7].text, tds[9].img['title'], tds[11].text, tds[11].a['href'].split("=")[1])
                try:
                    racename = tds[11].text
                    #print(racename)
                    # WIP: convert to dates?
                    # startdate = datetime.strptime(tds[3].text, '%d/%m/%Y')
                    startdate =tds[3].text

                    # no enddate, 1 day race
                    if tds[5].text != "\xa0":
                        # WIP: convert to dates?
                        # enddate = datetime.strptime(tds[5].text, '%d/%m/%Y')
                        enddate = tds[5].text
                    else:
                        enddate = tds[3].text
                    category = tds[7].text
                    category_id = categories[category]
                    try:
                        cqraceid = int(tds[11].a['href'].split("=")[1])
                    except:
                        continue
                    country = tds[9].img['title']

                    #print(cqraceid, racename, startdate, enddate, category, category_id, country)
                    #print(type(cqraceid), racename, type(startdate), type(enddate), category, type(category_id), country)
                    # exclude categories that we don't use
                    if category_id:
                        #races.append([cqraceid, racename, startdate, enddate, category_id, country])
                        bulkInsert([cqraceid, cqraceid, racename, startdate, enddate, int(category_id), country, year],1,)
                        scrape_results(cqraceid)
                    else:
                        print(f"{racename} has category {category}, do not store.")

                    try:
                        stages_id = tds[13].a['href'].split("=")[1]
                        if stages_id:
                            #url = "https://cqranking.com/men/asp/gen/"&stages
                            print("####################################")
                            print("FOUND STAGES")
                            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                            get_stages(racename, stages_id, year, category, country)

                    except:
                        continue
                except:
                    continue
        except:
            continue
    #write_to_csv(races)


def scrape_results(race):
    """
    This will get all results for one day races and GC for multi-day races.
    Still need to get stage results and leader jerseys for multi-day races.
    """
    base_result_url = "https://cqranking.com/men/asp/gen/race.asp?raceid="
    b = base_result_url + str(race)
    #print(b)
    r = requests.get(b)
    # print(r)
    soup = BeautifulSoup(r.text, "html.parser")
    # print(soup)
    # select the table which contains the results
    # first look for the class="tabrow1" or class="tabrow2"
    first_result = soup.find("td", ["tabrow1", "tabrow2"])
    #print(first_result)
    # then get the parent <tr>
    result_tr = first_result.parent
    #print(result_tr)
    # and its parent <table>
    result_table = result_tr.parent
    #print(result_table)

    row_tags = result_table.find_all('tr')[1:11] # skipping the header row, top 10 only
    #print("row_tags:", row_tags)
    # now we want to find all tr within this table
    # don't forget to replace the "leader" with an integer

    for row_tag in row_tags:
        try:
            tds = row_tag.find_all('td')
            print(tds[1].text)
            #print(tds[1].text.split(".")[0], tds[5].a['href'].split("=")[1], race)
            # # Now get all info in each cell
            # leader is missing with this method
            print(f"Text for leader found: { tds[1].text }")
            if tds[1].text == 'leader':
                print("###########################")
                print("We have found the leader. Only do this for GT1 and GT2")
                print("###########################")
                rank = 0
            else:
                rank = tds[1].text.split(".")[0]
            #print(int(rank))
            rider = tds[5].a['href'].split("=")[1]
            print(f"Resultaat: {rank}, {race}, {rider}")
            #results.append([rank, race, rider])
            bulkInsert([rank, race, rider], 2)
        except:
            continue
    

def get_stages(racename, race_id, year, category, country):
    """
    Called from scrape_calendar, to specifically get stages for multi-day-races
    """
    base_result_url = "https://cqranking.com/men/asp/gen/tour.asp?tourid="
    b = base_result_url + str(race_id)
    #print(b)
    r = requests.get(b)
    #print(r)
    soup = BeautifulSoup(r.text, "html.parser")
    # print(soup)
    # select the table which contains the results
    # first look for the class="tabrow1" or class="tabrow2"
    first_result = soup.find("td", ["tabrow1", "tabrow2"])
    #print(first_result)
    # then get the parent <tr>
    result_tr = first_result.parent
    #print(result_tr)
    # and its parent <table>
    result_table = result_tr.parent
    #print(result_table)

    row_tags = result_table.find_all('tr')[1:] # skipping the header row
    #print("row_tags:", row_tags)
    # now we want to find all tr within this table

    for row_tag in row_tags:
        try:
            tds = row_tag.find_all('td')
            # for t in tds:
            #     print(i, t.text)
            #     i +=1
            # 1 is date, year is missing
            # 7 is name of stage, add racename to it
            # 12 is rider who won stage

            #print(tds[7].text[0:5])
            startdate = tds[1].text +"/" + str(year)
            
            #print(lookupcat)
            
            #print(category, category_id)
            #print(startdate)
            fullname = racename +" "+ tds[7].text
            print(fullname, category)
            cqraceid = int(tds[7].a['href'].split("=")[1])
            print(f"Raceid = {cqraceid}")
            # Now add race to races:
            if tds[7].text[0:5] == "Stage":
                lookupcat = str(category)+"s"  
            elif tds[7].text[0:7] != "General": # Mountain and Points ranking
                lookupcat = str(category)+"r"
            if lookupcat:    
                print(lookupcat)
                category_id = categories[lookupcat]
                print(category_id)
                stagewinner = tds[11].a['href'].split("=")[1]
                print([cqraceid, cqraceid, fullname, startdate, startdate, int(category_id), country],1,)
                #stagewinner = tds[11].a['href'].split("=")[1]
                #print(1, cqraceid, stagewinner)
                # Add the race 
                bulkInsert([cqraceid, cqraceid, fullname, startdate, startdate, int(category_id), country, year],1,)
                # and add stage winnner
                #bulkInsert([1, cqraceid, stagewinner], 2)
                #print(f"Inserted stagewinner { stagewinner } for race { cqraceid }")
                # or, alternatively, scrape the stage results as if it's a 'normal' race
                scrape_results(cqraceid) #

        except:
            continue


def get_rider_info(riderid):
    BASE_RIDER_URL = "https://cqranking.com/men/asp/gen/rider.asp?riderid="
    b = BASE_RIDER_URL+str(riderid)

    #print(b)
    r = requests.get(b)
    #print(r)
    soup = BeautifulSoup(r.text, "html.parser")
    first_result = soup.find("table", "borderNoOpac")
    #print(first_result)
    next_table = first_result.find("table")
    #print(next_table)

    row_tags = next_table.find_all('tr') # skipping the header row
    #print("row_tags:", row_tags)
    # now we want to find all tr within this table

    tds = row_tags[0].find_all('td')
    name = tds[1].text.strip()
    #print(name)
    nationality = tds[1].img['alt'].strip()
    #print(nationality)
    tds = row_tags[1].find_all('td')
    birthdate = tds[1].text.strip()
    #print(birthdate)
    tds = row_tags[2].find_all('td')
    status = tds[1].text.strip()
    #print(status)
        # try:
        #     tds = row_tag.find_all('td')
        #     # first row [0], second td [1]: name + nationality
        #     name = row_tag[0][1].text
        #     print(name)
    bulkInsert([riderid, riderid, birthdate, name, nationality, False], 3)

        # except:
        #     print("rider {} bestaat niet".format(riderid))


def write_to_csv(races):
    with open('scraping/csv/2022/full_results.csv','a', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(races)

#for race in range(2010, 2020):
#    scrape_calendar(race)
#get_stages("Paris-Nice", 3895, 2021, "2.WT1", "Fra")


#bulkInsert([3, 3, '10001655448', 'CUNEGO Damiano', 'ITA', False], 3)

scrape_calendar(2022)

#https://cqranking.com/men/asp/gen/race.asp?raceid=39990

#scrape_results(40681)
