from daftlistings import Daft, RentType
import json
import sqlite3
import traceback
import json
import sys
import time

from math import sin, cos, sqrt, atan2, radians


def caldis(lat2,lon2, lat1,lon1):
    R = 6373.0
    #lat1 = radians(53.332119)
    #lon1 = radians(-6.230313)
    #lat2 = radians(53.341553)
    #lon2 = radians(-6.253255)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c * 1000



def calall(lat,lon):
    lat2 = radians(lat)
    lon2 = radians(lon)

    la_1 = radians(53.332119)
    lo_1 = radians(-6.230313)
    la_2 = radians(53.341553)
    lo_2 = radians(-6.253255)
    d1 = caldis(lat2,lon2,la_1,lo_1)
    d2 = caldis(lat2,lon2,la_2,lo_2)
    return d1,d2


def transPrice(v):
    realp = ""
    for c in v:
        if c >='0' and c <= '9':
            realp += c
    price = int(realp)
    if "Per week" in v:
        price = price / 7.0 * 30.0
    return price

#conn = sqlite3.connect('test.db')
f= open("res.json","w")
failink= open("fail_link","w")

daft = Daft()

daft.set_county("Dublin City")
daft.set_listing_type(RentType.ANY)
#daft.set_min_price(1000)
#daft.set_max_price(1500)


offset = 0

while 1:
    try:
        daft.set_offset(offset)
        print(offset)
        listings = daft.search()
        if not listings:
            break
        le = len(listings)
        offset += le
        print(listings[0].daft_link)
        #c = conn.cursor()
        for listing in listings:
            try:
                lati = float(listing.latitude)
                lon = float(listing.longitude)
                d1,d2 = calall(lati, lon)
                if d1 < 2000 and d2 < 2000:
                    t = listing.as_dict()
                    f.write(json.dumps(t))
                    f.write("\n")
                    f.flush()
                print(offset)
                #t['address'] = listing.formalised_address
                #t['link'] = listing.daft_link
                ##(listing.price/listing.bedrooms)
                #t['prices'] = transPrice(listing.price)/int(listing.bedrooms)
                #t['bedrooms'] = listing.bedrooms
                #t['city_center_distance'] = listing.city_center_distance
                #c.execute('INSERT INTO daft VALUES (?,?,?,?,?,?,?)', (t['link'], int(t['prices']), listing.price, t['bedrooms'], t['address'],t['city_center_distance'], int(listing.bathrooms)))
            except Exception as e:
                traceback.print_exc()
                print(e)
                print("fail link",listing.daft_link)
                failink.write(listing.daft_link)
                failink.write("\n")
                failink.flush()
        #conn.commit()
        sys.stdout.flush()
    except Exception as e:
        traceback.print_exc()
        print(e)
        offset+=1
        time.sleep(5)




sys.stdout.flush()
#conn.close()
f.close()
failink.close()



