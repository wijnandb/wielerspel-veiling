# This isn't working. Try insert_data-postgres

import csv
import sys
import os
from models import Race

# Full path and name to your csv file
csv_filepathname = "/home/wijnandb/Downloads/2019-calendar.csv"
# Full path to your django project directory
your_djangoproject_home = "/home/wijnandb/sites/heroku/wielerspel"


dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')

for row in dataReader:
    if row[0] != 'startdate':  # Ignore the header row, import everything else
        race.startdate = row[0]
        race.enddate = row[1]
        team.category = row[2]
        team.name = row[3]
        team.CQranking_id = row[5]
    team.save()
