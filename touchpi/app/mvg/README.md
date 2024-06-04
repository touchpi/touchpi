## mvg app

### Introduction
This app shows when a public transportation at a certain starting point will leave and when a connection of a second transportation will leave. 

The upper semicircle shows the departure times of the first transportation.

The lower semicircle shows the departure times of a second transportation.

### How to use
* Get your public transportation stop id
  * Go to Google maps and locate your latitude and longitude of your first stop
  * Enter the url in a browser for getting a station id: https://www.mvg.de/api/fib/v2/station/nearby?latitude=nn.nnnnnnnnnnnnnnn&longitude=nn.nnnnnnnnnnnnnnn (replace nn.nnn)
  * Search for the globalID
* Create your URL for getting the departure times. 
  * Use the globalID.
  * Filter your transport types
  * Plan your offset of the start time. If you need 5 min from your location to the public transportation stop, then add 5 min offsetInMinutes
  * Update your mvg_public_transport_url1 in mvg.local.toml 
* Create your second URL analogues
  * For your second transportation add more offsetInMinutes. You want to check which transports a reachable. 
* Set destination of transports
  * Find in the MVG plans all possible destinations for your transports.
  * You can also just call the created URLs in the browser at different times and get the destinations there
  * Update your destination filter for both transportation in mvg_possible_destination in mvg.local.toml
* Change some colors in your mvg.local.toml file
Have fun 

### More information
* Developer note 15.07.2023:
  * Old api (not suported since 01.07.2023):
    * Get station id: https://www.mvg.de/api/fahrinfo/location/queryWeb?q=Pasing
    * Get schedule at station https://www.mvg.de/api/fahrinfo/departure/de:09162:10?footway=0
      * Offset of start time in minutes: &footway=0
      * Id of bus station Schmaedelstraße:      de:09162:1844
      * Id of bus station Erna-Eckstein-Strasse: de:09162:1858
      * Id of mixed station Pasing Hbf:         de:09162:10
  * Api v2 (actual):
    * Info for developer: https://www.mvv-muenchen.de/fahrplanauskunft/fuer-entwickler/index.html
    * An api example: https://github.com/toebsen/python_mvg_api/blob/master/mvg_api/__init__.py
    * Get station id (sample for Laim): https://www.mvg.de/api/fib/v2/station/nearby?latitude=48.14462069791742&longitude=11.502655363751208
    * Get schedule at station https://www.mvg.de/api/fib/v2/departure?globalId=de:09162:9
    * Station ids are unchanged (see old version).
      * Can be found in a CVS of MVG: https://www.mvv-muenchen.de/fahrplanauskunft/fuer-entwickler/opendata/index.html
    * Offset of start time in minutes: &offsetInMinutes=5
    * Filter for transport types: &transportTypes=UBAHN,TRAM,BUS,SBAHN,SCHIFF
    * Limit of result set(?): &limit=20


