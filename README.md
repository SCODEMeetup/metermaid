Hotspots by Metermaid
=====================

Find parking hotspots in columbus.

### Use Case
https://www.smartcolumbusos.com/data-stories/parking-tickets-piling-up-use-data-to-determine-why

### Tech Stack
  1. Python
  2. Bokeh - Interactive visualization library https://bokeh.pydata.org/en/latest/
  3. Litespeed (web-server) - https://www.litespeedtech.com/products/litespeed-web-server
  4. Pandas - Data analysis library  https://pandas.pydata.org/
  5. PyCharm SE - IDE
  6. Google maps platform - key registration 

### Installation 
  Running the application
  1. Clone repo to your local https://github.com/allparks/metermaid.git
  2. Install lite-server 
    1. `sudo npm install -g lite-server`
  3. In terminal navigate to '/metermaid/parkingApp' dir
  4. type `lite-server` to start the server and load the app.    


### Data Used

https://www.smartcolumbusos.com/data

1. Mapping meter count = Parking Meters + Parking transaction data (2015-2017)
   1. Parking Meters -
      1. Longitude x/ Latitude y/
   2. Parking transaction data (2015-2017) -
      1. Longitude and latitude
      2. count (meter ids)
      3. meter_id <inner join> pole 
2. Geotab data (Searching For Parking) - How many people are trying to park with different time frames
   1. sum (Avg. time to park searching)
   2. Avg (Total searching )
   3. Parking geohash
   4. Distinct value Longitude
   5. Distinct value Latitude
   6. location and hourly, avg park time
3. Violations (Columbus City Parking Violations and Ticket Status 2013-2018) + Parking meters
   1. inner join (meter id)
   2. Longitude / Latitude
   3. count (ticket_id)
4. Points of interests
   1. POI Type (edited)

### Team

### Presentation
[Finding Parking Hotspots](https://github.com/allparks/metermaid/blob/master/presentations/HotSpots-Deck.pdf)

### Screen Shots

