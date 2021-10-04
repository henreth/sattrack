import requests
import json
import ephem
from datetime import datetime
from bs4 import BeautifulSoup

##### FOR MORE SATELLITE DETAILS
ITSwebexample = 'https://in-the-sky.org//spacecraft.php?id=20580&skin=1'
#replace 20580 with any NORAD, scrape details including name, categories, launch site, launch date, owner
noradid = '25544'
itsweb = 'https://in-the-sky.org//spacecraft.php?id=' + noradid 


n2yoexmple = 'https://www.n2yo.com/satellite/?s=25994'
# same as above



#### SATELLITE CLASS
class Satellite:
    
    def __init__(self,name,norad,line1,line2,title,altname,status,owner,cat,launch,site,flightend,**kwargs):
        self.name = name
        self.norad = norad
        self.line1 = line1
        self.line2 = line2
        
        self.title = title
        self.altname = altname
        self.status = status
        self.owner = owner
        self.categories = cat
        self.ld = launch
        self.ls = site
        self.fe = flightend


    def locate(self):
        tle_rec = ephem.readtle(self.name,self.line1,self.line2)
        tle_rec.compute()
        today = str(datetime.today()) 
        print("Location of " + str(self.name) + " at " + today + ":")
        print("Longitude: " + str(tle_rec.sublong))
        print("Latitude: " + str(tle_rec.sublat))
        

    def categories(self):
        print("Categories:")
        if len(categories) > 1:
            for i in categories:
                print(i)
        elif len(categories) == 1:
            print(categories)

    def launchInfo(self):
        print("Launch Date: " + ld)
        print("Launch Site: " + ls)
        print("Flight Ended: " + fe)

    def __str__(self):
            return str(self.name) + "\r\n" + self.norad + "\r\n" + self.line1 + '\r\n' + self.line2

##iss = Satellite("International Space Station","25544","line1","line2", "Station")


#### MASTER LISTS:
norad_list= []
msl = {}

################ SPACE STATIONS
cs_stat = 'http://www.celestrak.com/NORAD/elements/stations.txt'

req = requests.get(cs_stat).text
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

for i in d2:
    norad_list.append(i[2][2:7],
        )
norad_list.sort()


d4 = {}
for i in d2:
    d4[i[0].strip(" ")]= ({
        "NORAD": i[2][2:7],
        "Line 1": i[1],
        "Line 2": i[2]
        })


#### satellite info:
    
##noradid = '25544'
itsweb = 'https://in-the-sky.org//spacecraft.php?id=' 
sat_list = {}
for i in norad_list:
    print(i)
    url = itsweb + i
    data = requests.get(url).text
    soup = BeautifulSoup(data,'html.parser')
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
       ls4 = ls4.replace(" (Also known as Baikonur Cosmodrome)",'')
    

    ### DATA COLLECTION
    sat_list[i] = ({
        "Title": title,
        "Name": name4,
        "Status": status3,
        "Owner": owner4,
        "Categories": cata,
        "Launch Date": launch3,
        "Flight Ended": fe3,
        "Launch Site": ls4
        })
    
##    sat_list_info.append({
##        "Title": title,
##        "Name": name4,
##        "Status": status3,
##        "Owner": owner4,
##        "Categories": cata,
##        "Launch Date": launch3,
##        "Flight Ended": fe3,
##        "Launch Site": ls4
##        })
    
d6 = {}
for i in d2:
    d6[i[2][2:7]] =  {
        i[0].strip(" "),
        i[2][2:7],
        i[1],i[2]}

d6['25544'].append(ls4)

##for i in d2:
##    msl[i[2][2:7]] =  Satellite(
##        i[0].strip(" "),
##        i[2][2:7],
##        i[1],i[2],
####        sat_list[i][
##            )




##################### SCIENCE SATELLITES
##cs_sci = 'http://www.celestrak.com/NORAD/elements/science.txt'
##
##req_sci = requests.get(cs_sci).text
##data_sci = BeautifulSoup(req_sci,'html.parser')
##dt1_sci = str(data_sci)
##dt2_sci = dt1_sci.split('\r\n')
##ldt_sci = len(dt2_sci)
##d_sci = {e for i, e in enumerate(zip(*[iter(dt2_sci)]*3), 1)}
##d2_sci = list(d_sci)
##
##for i in d2_sci:
####    d5[i[0].strip(" ")] =  Satellite(i[0].strip(" "),i[2][2:8],i[1],i[2])
##    Master_Sat_List[i[2][2:7]] =  Satellite(i[0].strip(" "),i[2][2:7],i[1],i[2],"Science-Satellite")
##
##for i in d2_sci:
##    norad_list.append(i[2][2:7],
##        )
##norad_list.sort()
##
##msl = Master_Sat_List


##################### ALL ACTIVE SATELLITES
##cs_act = 'http://www.celestrak.com/NORAD/elements/active.txt'
##
##req_act = requests.get(cs_act).text
##data_act = BeautifulSoup(req_act,'html.parser')
##dt1_act = str(data_act)
##dt2_act = dt1_act.split('\r\n')
##ldt_act = len(dt2_act)
##d_act = {e for i, e in enumerate(zip(*[iter(dt2_act)]*3), 1)}
##d2_act = list(d_act)
##
##for i in d2_act:
####    d5[i[0].strip(" ")] =  Satellite(i[0].strip(" "),i[2][2:8],i[1],i[2])
##    Master_Sat_List[i[2][2:7]] =  Satellite(i[0].strip(" "),i[2][2:7],i[1],i[2])
##
##for i in d2_act:
##    norad_list.append(i[2][2:7],
##        )
##norad_list.sort()
##
##msl = Master_Sat_List
