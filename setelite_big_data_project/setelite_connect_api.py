from itertools import cycle

import requests
import geocoder
from time import sleep
import json
from kafka import KafkaProducer



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
def postition():
    try:
        latitude,longitude=None,None
        g = geocoder.ip('me')

        latitude, longitude = g.latlng[0],g.latlng[1]
        return latitude,longitude
    except Exception as e:
            print(e)
            return latitude, longitude,


def get_posts(noaa_id,latitude,longitude):
    url = f'https://api.n2yo.com/rest/v1/satellite/positions/{noaa_id}/{latitude}/{longitude}/0/2/&apiKey=YMY6UM-W9NPTJ-L2A7K4-5ERX'

    try:
        response = requests.get(url)
        if response.status_code == 200:
            posts = response.json()
            return posts
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        sleep(.5)
        return None
producer=KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x:json.dumps(x).encode('utf-8'),acks='all')
def main():
    while True:
        latitude,longitude=postition()
        if latitude!= None:
            for v in cycle(satellites.values()):
                data=dict()
                posts = get_posts(v,latitude,longitude)
                if posts !=None:
                    data=posts
                    producer.send(topic="satelite",value=data)
                    print(posts)
                    sleep(2)
        sleep(1)


if __name__ == '__main__':
    main()
