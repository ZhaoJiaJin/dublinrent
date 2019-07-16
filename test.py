from daftlistings import Daft, RentType
import json
import sqlite3
import traceback
import sys
import time





def transPrice(v):
    realp = ""
    for c in v:
        if c >='0' and c <= '9':
            realp += c
    price = int(realp)
    if "Per week" in v:
        price = price / 7.0 * 30.0
    return price



conn = sqlite3.connect('test.db')

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
        c = conn.cursor()
        for listing in listings:
            try:
                t = {}
                t['address'] = listing.formalised_address
                t['link'] = listing.daft_link
                #(listing.price/listing.bedrooms)
                t['prices'] = transPrice(listing.price)/int(listing.bedrooms)
                t['bedrooms'] = listing.bedrooms
                t['city_center_distance'] = listing.city_center_distance
                c.execute('INSERT INTO daft VALUES (?,?,?,?,?,?,?)', (t['link'], int(t['prices']), listing.price, t['bedrooms'], t['address'],t['city_center_distance'], int(listing.bathrooms)))
            except Exception as e:
                traceback.print_exc()
                print(e)
                print("fail link",listing.daft_link)
        conn.commit()
        sys.stdout.flush()
    except Exception as e:
        traceback.print_exc()
        print(e)
        offset+=1
        time.sleep(5)




sys.stdout.flush()
conn.close()




