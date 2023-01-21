def main():
    add_tc()

# read csv file ploegen.csv


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
        print(result)
        for rider in sold_riders[1:]:
            # if rider == rider
            if result[3] == rider[0]:
                print(f"{result[3]} == {rider[0]}")
                # add tc to result
                result.append[rider[3]]
    print(result)
    #updated_results.append(result)
    
    # create new csv file results_points_teamcaptain.csv
    with open('scraping/csv/2023/results_points_teamcaptain.csv', 'w') as f:
        write = csv.writer(f)
        write.writerows(updated_results)

if __name__ == "__main__":
    main()
