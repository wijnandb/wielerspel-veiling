import requests
from bs4 import BeautifulSoup

startURL = 'https://cqranking.com/men/asp/gen/'

# Here comes the list of all races in the season
# id's are CQRanking ID's
race_calendar = [["2/03/2019", "", "1.1", "Classic d'Ardèche", "race.asp?raceid=34510", ""],
                 ["2/03/2019", "", "1.WT3", "Omloop Het Nieuwsblad", "race.asp?raceid=34511", ""],
                 ["10/03/2019", "17/03/2019", "2.WT1", "Paris - Nice", "race.asp?raceid=34788", "tour.asp?tourid=3541"]]


results = []


# start with 1-day races and final rankings tours
for race in race_calendar:
    try:
        b = startURL + str(race[4])
        # print(b)
        r = requests.get(b)
        print(r)
        soup = BeautifulSoup(r.text, "html.parser")
        # print(soup)
        # select the table which contains the results
        # first look for the class="tabrow1" or class="tabrow2"
        first_result = soup.find("td", ["tabrow1", "tabrow2"])
        # print(first_result)
        # then get the parent <tr>
        result_tr = first_result.parent
        # print(result_tr)
        # and its parent <table>
        result_table = result_tr.parent
        # print(result_table)
        row_tags = result_table.find_all('tr')
        # print("row_tags:", row_tags)
        # now we want to find all tr within this table

        for row_tag in row_tags:

            # Now get all info in each cell
            row = [col.text for col in row_tag.find('td')]
            print(row)
            # we want to get the A HREF from certain cells as well
            results.append(row)  # Add this row to all the other rows of this table
#                        df = df.append(results)
    except:
        continue

print(results)
# df = pd.DataFrame(results)
# print(df)


#                df.insert(0,'race',race[3])
#                df.insert(1, 'raceID',race[2])
#                df = df.drop(df.index[0:1])
#                print("drop index[0:4]",df)
#                df = df.drop(df.index[-1:0])
#                print(df)
#                with open('2019_final_rankings.csv', 'a') as f:
#                        df.to_csv(f, index = False)
