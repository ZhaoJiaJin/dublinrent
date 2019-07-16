from daftlistings import Daft, RentType
import json




def transPrice(v):
    realp = ""
    for c in v:
        if c >='0' and c <= '9':
            realp += c
    price = int(realp)
    if "Per week" in v:
        price = price / 7.0 * 30.0
    return price




daft = Daft()

daft.set_county("Dublin City")
daft.set_listing_type(RentType.ANY)
#daft.set_min_price(1000)
#daft.set_max_price(1500)


offset = 0

with open("result","a+") as f:
    while 1:
        daft.set_offset(offset)
        listings = daft.search()
        if not listings:
            break
        le = len(listings)
        offset += le
        for listing in listings:
            tmpres = {}
            tmpres['address'] = listing.formalised_address
            tmpres['link'] = listing.daft_link
            #print(listing.price/listing.bedrooms)
            tmpres['prices'] = transPrice(listing.price)/listing.bedrooms
            tmpres['bedrooms'] = listing.bedrooms
            tmpres['city_center_distance'] = listing.city_center_distance
            f.write(json.dumps(tmpres))
            f.write("\n")
            f.flush()





