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
            print("insert races")
            sql_insert_query = """INSERT into results_race(id, cqraceid, name, startdate, enddate, category_id, country) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
# this is query for results
        elif type==2:
            print("insert results")
            sql_insert_query = """INSERT into results_uitslag(rank, race_id, rider_id) VALUES (%s, %s, %s)"""
        elif type==3:
            sql_insert_query = """ INSERT into results_rider(name, birthday, cqriderid)
                            VALUES (%s, %s, %s) """
        # executemany() to insert multiple rows rows
        else:
            print("failed to find correct query")
        cursor.execute(sql_insert_query, records,)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into table")

    except (Exception, psycopg2.Error) as error:
        print("Failed inserting record into table {}".format(error))

    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


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
    'NC.1': 14,
    'NC.2': 15,
    'NC.3': 16,
    'NC.4': 17,
    'NC.5': 18,
    'NCT.1': 19,
    'NCT.2': 20,
    'NCT.3': 21,
    'NCT.4': 22,
    'NCT.5': 23,
    'CC1': 24,
    'CC2': 25,
    'CCT1': 26,
    'CCT2': 27,
    'GT2r': 36,
    'GT1r': 35,
    'GT2s': 34,
    'GT1s': 33,
    '2.WT3s': 32,
    '2.WT2s': 31,
    '2.WT1s': 30,
    '2.PSs': 29,
    '2.1s': 28,
    '2.WT3r': 39,
    '2.WT2r': 38,
    '2.WT1r': 37,
}
races = []
results = []
riders = []
def scrape_calendar(year):
        
    for i in range(1,13):
        try:
            b = startURL+str(year)+"&month="+str(i)
            print(b)
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
                # we skip the header row, hence [1:12] and only top 10
                tds = tr.find_all('td')
                #print (tds[3].text, tds[5].text, tds[7].text, tds[9].img['title'], tds[11].text, tds[11].a['href'].split("=")[1])
                try:
                    racename = tds[11].text
                    #print(racename)
                    startdate = datetime.strptime(tds[3].text, '%d/%m/%Y')
                    # no enddate, 1 day race
                    if tds[5].text != "\xa0":
                        enddate = datetime.strptime(tds[5].text, '%d/%m/%Y')
                    else:
                        enddate = ""
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
                        bulkInsert([cqraceid, cqraceid, racename, startdate, enddate, int(category_id), country],1,)
                        scrape_results(cqraceid)
                    else:
                        print(f"{racename} has category {category}, do not store.")

                    try:
                        stages_id = tds[13].a['href'].split("=")[1]
                        if stages_id:
                            #url = "https://cqranking.com/men/asp/gen/"&stages
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

    row_tags = result_table.find_all('tr')[1:12] # skipping the header row, top 10 only
    #print("row_tags:", row_tags)
    # now we want to find all tr within this table

    for row_tag in row_tags:
        try:
            tds = row_tag.find_all('td')
            #print(tds[1].text.split(".")[0], tds[5].a['href'].split("=")[1], race)
            # # Now get all info in each cell
            rank = tds[1].text.split(".")[0]
            #print(int(rank))
            rider = tds[5].a['href'].split("=")[1]
            #print(f"Resultaat: {rank}, {race}, {rider}")
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
    print(b)
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
                bulkInsert([cqraceid, cqraceid, fullname, startdate, startdate, int(category_id), country],1,)
                print([cqraceid, cqraceid, fullname, startdate, startdate, int(category_id), country],1,)
                # and add stage winnner to results:
                stagewinner = tds[11].a['href'].split("=")[1]
                #print(1, cqraceid, stagewinner)
                bulkInsert([1, cqraceid, stagewinner], 2)
        except:
            continue


def get_rider_info(riderid):
    BASE_RIDER_URL = "https://cqranking.com/men/asp/gen/rider.asp?riderid="
    b = BASE_RIDER_URL+str(riderid)
    """
    r = requests.get(b)
    soup = BeautifulSoup(r.text, "html.parser")
    first_result = soup.find("td", ["raceheader"])
        # now get the parent tr
    result_tr = first_result.parent
    # and the parent table
    table = result_tr.parent
    table_rows = table.find_all('tr')
    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        print(row)
    """
    try:
        dfs = pd.read_html(b)
        #print(type(dfs))
        #print(len(dfs))
        relevant_df = dfs[8][1]
        renner_info = relevant_df.values.tolist()
        renner_info.append(riderid)
        #print(renner_info)
        riders.append(renner_info)
    except:
        print("rider {} bestaat niet".format(riderid))


def write_to_csv(races):
    with open('scraping/csv/scraped_races.csv','a', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(races)

scrape_calendar(2021)
#get_stages("Paris-Nice", 3895, 2021, "2.WT1", "Fra")
