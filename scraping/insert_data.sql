/* script to run from commandline PSQL, to fill wielerspel database with data
 first fill the countrycodes into the country table 
*/
COPY results_Category FROM '/home/wijnandb/Downloads/2019_calendar - Categories.csv';

/*
INSERT INTO results_Edition (year) VALUES
(2017),
(2018),
(2019),
(2020);
*/

COPY results_RacePoints FROM '/home/wijnandb/Downloads/2019_calendar - Racepoints.csv';

