import requests
from bs4 import BeautifulSoup
import pandas as pd

startURL = 'https://cqranking.com/men/asp/gen/race.asp?raceid='

# Here comes the list of all races in the season
# id's are CQRanking ID's
race_calendar = [39210]


results = []


# start with 1-day races and final rankings tours
for race in race_calendar:
    """
    This will get all results for one day races and GC for multi-day races.
    Still need to get stage results and leader jerseys for multi-day races
    """
    try:
        b = startURL + str(race)
        print(b)
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

        row_tags = result_table.find_all('tr')[1:]
        for r in row_tags:
            print(r)
        #print("row_tags:", row_tags)
        # now we want to find all tr within this table

        for row_tag in row_tags:
            tds = row_tag.find_all('td')
            #print(tds[1].text.split(".")[0], tds[5].a['href'].split("=")[1], race)
            # # Now get all info in each cell
            position = tds[1].text.split(".")[0]
            rider = tds[5].a['href'].split("=")[1]
            print(f"Resultaat: {position}, {rider}, {race}")


    except:
        continue

# print(results)
# df = pd.DataFrame(results)
# print(df)


# df.insert(0,'race',race[3])
# df.insert(1, 'raceID',race[2])
# df = df.drop(df.index[0:1])
# print("drop index[0:4]",df)
# df = df.drop(df.index[-1:0])
# print(df)
# with open('scraping/csv/2021_final_rankings.csv', 'a') as f:
#     df.to_csv(f, index = False)
