import requests
import json
from datetime import datetime
import ephem

#####Process
# Load list of satellites
# Select one
# Options - [view info, coordinates, short summary, history]


celestrak = 'http://www.celestrak.com/NORAD/elements/stations.txt'

dt1 = datetime.today()
req = requests.get("http://api.open-notify.org/iss-now.json")
data = req.json()
dt = data['timestamp']
dt = datetime.fromtimestamp(dt)
dt2 = datetime.strftime(dt,'%Y-%m-%d %H-%M-%S')

iss_lat = data['iss_position']['latitude']
iss_lon = data['iss_position']['longitude']

###HUBBLE REFERED TO AS HST
hubble = '20580'
hbn = "Hubble Space Telescope"

###ISS REFERRED TO AS ZARYA
zarya = '25544'
zrn = "International Space Station"

while True:
    print("1: Hubble ")
    print("2: ISS ")
    satpre = int(input("Your Selection: "))
    satreq = ''
    if satpre == 1:
        satreq = hubble
        satname = hbn
    elif satpre == 2:
        satreq = zarya
        satname = zrn
        
    tle_url= 'http://tle.ivanstanojevic.me/api/tle/' + satreq
    tle_req = requests.get(tle_url)
    tle_data = tle_req.json()

    name = tle_data['name']
    line1 = tle_data['line1']
    line2 = tle_data['line2']

    tle_rec = ephem.readtle(name, line1, line2)
    tle_rec.compute()
    
    print(" ")
    print(satname,"\n"+dt2,"\nLongitude: " + str(tle_rec.sublong),"\nLatitude: " + str(tle_rec.sublat))
    print(" ")
