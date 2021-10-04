import requests
import json
import ephem
from datetime import datetime
from bs4 import BeautifulSoup


### List of sats
csel = 'http://www.celestrak.com/NORAD/elements/'

sc = 'science.txt'
ed = 'education.txt'
st = 'stations.txt'
eg = 'engineering.txt'
wt = 'weather.txt'
# from launches in the last 30 days
new = 'tle-new.txt'
# currently active 
act = 'active.txt'
# starlink
starlink = 'starlink.txt'

ed_sat = csel + ed

req = requests.get(ed_sat).text
data = BeautifulSoup(req,'html.parser')
dt1 = str(data)
dt2 = dt1.split('\r\n')
ldt = len(dt2)
d = {e for i, e in enumerate(zip(*[iter(dt2)]*3), 1)}
d2 = list(d)
d3 = []
for i in d2:
    d3.append({
        "Name": i[0].strip(" "),
        "NORAD": i[2][2:7],
        "Line 1": i[1],
        "Line 2": i[2]
        })

##### NORAD LIST 
nl = []
for i in d2:
    nl.append(i[2][2:7],
        )
nl.sort()

##### NORAD AND TLE

il = {}
for i in d2:
    il[i[2][2:7]]= ({
        "NORAD": i[2][2:7],
        "Line 1": i[1],
        "Line 2": i[2]
        })

##il = []
##for i in d2:
##    il[i] = ({i[0].strip(" "),i[2][2:7], i[1], i[2]})


#### satellite info:
    
##noradid = '25544'
itsweb = 'https://in-the-sky.org//spacecraft.php?id=' 
sl = {}


##for i in nl:
##    sl[i] = ({
##        "test":''
##        })
##

for i in range(len(nl)):
    norad = nl[i]
##    print(i)

    ##### URL formula
    url = itsweb + norad
    data = requests.get(url).text
    soup = BeautifulSoup(data,'html.parser')

    #### Title
    title1  = soup.find('p', attrs= {'class':'widetitle_sa'})
    title2 = str(title1).strip('<p class="widetitle_sa">')
    title = title2.strip('</p>')

    #### INFO
    infom = soup.findAll('table', attrs={'class':'objinfo'})                        
    infom1 = str(infom)

    #### NAME
    if len(infom1.split("Alternative names")) == 2:
        name2 = infom1.split("Alternative names")[1]
        name3 = name2.split("<br/>")
        if len(name3) == 2:
            name4 = name3[0].strip("</td>\n<td>\n").strip(" ")
        elif len(name3) > 2:
            name4 = []
            for i in range(len(name3)-1):
                namei = name3[i].strip("</td>\n<td>\n").strip(" ")
                name4.append(namei)
    elif len(infom1.split("Alternative names")) != 2:
        name4 = " "

    #### STATUS
    status1 = infom1.split("Status")[1]
    status2 = status1.split("</td>\n</tr>\n<tr>\n<td>")[0]
    status3 = status2.strip("</td>\n<td>")
    if status3 == 'Decaye':
        status3 = status3 + 'd'

    #### OWNER
    try:
        owner1 = infom1.split("Owner")[1]
        owner2 = owner1.split("</a>\n</td>\n</tr>\n<tr>\n<td>")[0]
        owner3 = owner2.strip("</td>\n<td>\n<a").strip(" ")
        owner4 = owner3.split(">\n")[1].strip(" ")
    except IndexError:
        owner4 = "-"

    #### CATEGORIES
    if infom1.find('Category') == -1 and infom1.find("Categories") != -1:
        cat1 = infom1.split("Categories")[1]
        cat2 = cat1.split("href=")
        cata = []
        for i in range(1,len(cat2)-4):
            cat3 = cat2[i].split("</a>\n</td>\n</tr>\n<tr>\n<td>")[0]
            cat4 = cat3.split("</a>\n<br/>\n<a")[0]
            cat5 = cat4.split(">\n")[1].strip(" ").strip("</a").strip(" ").replace("&amp;","&")
            cat5 = cat5.split()
            cat6 = ""
            for i in range(len(cat5)):
                cat6 += cat5[i].capitalize()
                if i == len(cat5) - 1:
                    pass
                else:
                    cat6 += " "
            cata.append(cat6)
    elif infom1.find('Category') > -1:
        cat1 = infom1.split("Category")[1]
        cat2 = cat1.split("</a>\n</td>\n</tr>\n<tr>\n<td>")[0]
        cat3 = cat2.strip("</td>\n<td>\n<a").strip(" ")
        cat4 = cat3.split(">\n")[1].strip('</a').strip(" ")
        cat5 = cat4.split()
        cat6 = ""
        for i in range(len(cat5)):
            cat6 += cat5[i].capitalize()
            if i == len(cat5) - 1:
                pass
            else:
                cat6 += " "
    else:
        cat6 = '-'

    #### LAUNCH DATE
    launch1 = infom1.split("Launched")[1]
    launch2 = launch1.split("</td>\n</tr>\n<tr>\n<td>")[0]
    launch3 = launch2.strip("</td>\n<td>")

    #### FLIGHT END
    fe1 = infom1.split("Flight ended")[1]
    fe2 = fe1.split("</td>\n</tr>\n<tr>\n<td>")[0]
    fe3 = fe2.strip("</td>\n<td>").strip(" ")

    #### LAUNCH SITE
    ls1 = infom1.split("Launch site")[1]
    ls2 = ls1.split("</a>\n</td>\n</tr>\n<tr>\n<td>")[0]
    ls3 = ls2.strip("</td>\n<td>\n<a").strip(" ")
    ls4 = ls3.split(">\n")[1].strip(" ")
    if ls4 == 'Tyuratam Missile and Space Center, Kazakhstan (Also known as Baikonur Cosmodrome)':
##       ls4 = ls4.replace(" (Also known as Baikonur Cosmodrome)",'')
        ls4 = 'Baikonur Cosmodrome, Kazakhstan'
    

    ### DATA COLLECTION
    sl[norad] = ({
        "Title": title,
        "NORAD": norad,
        "Name": name4,
        "Status": status3,
        "Owner": owner4,
        "Categories": cata,
        "Launch Date": launch3,
        "Flight Ended": fe3,
        "Launch Site": ls4,
        "Line1": il[norad]['Line 1'],
        "Line2": il[norad]['Line 2']
        })
    
