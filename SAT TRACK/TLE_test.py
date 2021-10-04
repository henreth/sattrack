import ephem
import datetime
import requests
import json


name = "ISS (ZARYA)"
line1 = "1 25544U 98067A   21113.19226883  .00001962  00000-0  43876-4 0  9997"
line2 = "2 25544  51.6444 254.7401 0002615 265.6775 152.4691 15.48922692280074"

tle_rec = ephem.readtle(name, line1, line2)
tle_rec.compute()

print(tle_rec.sublong, tle_rec.sublat)

tle_url= 'http://tle.ivanstanojevic.me/api/tle/' + '25544'
tle_req = requests.get(tle_url)
tle_data = tle_req.json()
