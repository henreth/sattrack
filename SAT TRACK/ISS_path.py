import requests
import pandas as pd
import datetime
import time

url = 'http://api.open-notify.org/iss-now.json'
date = datetime.datetime.now().strftime('%Y%m%d%H%M')
start_time = time.time()

ISS_data = []
while True:
    r = requests.get(url)

    ISS_loc =(r.json())

    ISS_data.append([
        ISS_loc['timestamp'],
        ISS_loc['iss_position']['latitude'],
        ISS_loc['iss_position']['longitude']
                    ])

    #write info to file

    df = pd.DataFrame(ISS_data,columns=['timestamp','latitude','longitude',])
    df.to_csv('ISS_loc_'+date+'.csv',index=None)

    if len(ISS_data) > 18000:
        break

    time.sleep(60.0 - ((time.time() - start_time) % 60))
