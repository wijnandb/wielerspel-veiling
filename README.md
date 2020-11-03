# Cyclinggame
Game played by 15 friends around UCI cycling races. 
Once a year, riders get auctioned. Every participating teamcaptain has 100 points to spend, for which they have to buy a minimum of 10 riders and a maximum of 30 riders.

During the year, getting results in UCI races rsults in earning points. Point system can slightly vary from year to year.

The application is a Django application, consisting of various ~~apps~~:

## Riders
These are the riders the teamcaptains can choose from during the auction. They are taken from [CQ ranking](https://cqranking.com/men/asp/gen/start.asp),
but can be taken from [Procyclingstats](https://www.procyclingstats.com/) or [Firstcycling](https://firstcycling.com/).

## Auction
During the auction, riders get sold. Highest bidder takes the rider (the actual auction is a live, f2f event, only the results need to be stored here).

A sale is registered in a model consisting of FK User(this is the teamcaptain), FK rider, year, price. 
We might add a timestamp to this.

On the [current website](https://wielerspel.com/veiling-de-ploegen/) there is a section with example pages:
- available, [unsold riders](https://wielerspel.com/veiling-2021-niet-verkochte-renners/)
- [sold riders](https://wielerspel.com/veiling-de-ploegen/), owned by a teamcaptain
- [overview of situation during the auction](https://wielerspel.com/veiling-2021-overzicht-landen/): how many riders does each teamcaptain have, how much points have they spend, what is maximum bid on next rider

## Results
The results will be scraped, see the separate app "Scraping" fro more details. We intentionally have a separate app for storing the results, which ideally 
consists of more than just the bare necessities and contains extra information about riders, connects races from one year to another and shows which team a rider
belongs to.

## Scraping
The most important part of the results is which rider finishes in which position in what category race. This sounds obvious and it is, but it means we have 
some options when it comes to the logic of our scraper. Each of the proposed scraping sites has an overview page per rider, detailing the results per year, like 
[the results of Hugh Carthy in 2020 on CQ ranking](https://cqranking.com/men/asp/gen/rider_palm.asp?riderid=21014&year=2020&all=0&current=0).

This means we could simply scrape the results from the riders that are sold, looping over each rider in a team and getting the results. This would be good enough 
for the first version.

## Points



