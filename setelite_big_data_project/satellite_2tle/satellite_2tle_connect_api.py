from ensurepip import bootstrap

import requests as re
import json
import time
from kafka import KafkaProducer
from matplotlib.font_manager import json_dump
from torch.utils.hipify.hipify_python import value

satellites = {
    "International Space Station (ISS)": 25544,
    "Hubble Space Telescope": 20580,
    "Terra (EOS AM-1)": 25994,
    "Aqua (EOS PM-1)": 27424,
    "Landsat 8": 39084,
    "Sentinel-1A": 39634,
    "Sentinel-2A": 40697,
    "Sentinel-3A": 41335,
    "Envisat": 27386,
    "Jason-3": 41240,
    "CALIPSO": 29108,
    "CloudSat": 29107,
    "SMAP": 40376,
    "Suomi NPP": 37849,
    "INSAT-3A": 27714,
    "INSAT-3C": 27298,
    "INSAT-3DR": 41752,
    "GSAT-6": 40880,
    "GSAT-7": 39234,
    "GSAT-10": 38779,
    "GSAT-12": 37746,
    "GSAT-14": 39498,
    "GSAT-15": 41028,
    "GSAT-16": 40332,
    "GSAT-18": 41793,
    "GSAT-19": 42747,
    "GSAT-29": 43651,
    "GSAT-30": 45026,
    "GSAT-31": 44034,
    "GSAT-6A": 43241,
    "GSAT-7A": 43864,
    "GSAT-9": 42691,
    "RISAT-1": 38248,
    "Cartosat-1": 28649,
    "Cartosat-2C": 41599,
    "Cartosat-2D": 42063,
    "Cartosat-2E": 42767,
    "Cartosat-3": 44804
}
def satellite_2tle_connect(satid):
    url=f"https://api.n2yo.com/rest/v1/satellite/tle/{satid}&apiKey=YMY6UM-W9NPTJ-L2A7K4-5ERX"
    try:
        response=re.get(url)
        if response.status_code==200:
            return response.json()
    except re.exceptions.RequestException as e:
        print('Error:', e)
        return None
producer=KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x:json_dump(x).encode('utf-8'))
def main():

    for k,v in satellites.items():
        data=dict()
        satellites_2tle=satellite_2tle_connect(v)

        data['satid'],data['satname'],data['transactionscount']=tuple(satellites_2tle['info'].values())
        print(data['satid'],data['satname'],data['transactionscount'])
        line1=[i for i in satellites_2tle['tle'].split("\r\n")[0].split(" ") if i!=""]
        line2 =[ i for i in satellites_2tle['tle'].split("\r\n")[1].split(" ") if i!=""]
        print(line1,line2)




if __name__=='__main__':
   main()