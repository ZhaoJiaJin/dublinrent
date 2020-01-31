#!/usr/bin/env python

import json


with open("res.json","r") as f:
    for l in f.readlines():
        l = l.strip()
        d = json.loads(l)
        try:
            price = float(d["price"])
            beds = float(d["num_bedrooms"])
            if price/beds < 1000:
                print(d["daft_link"])
        except Exception as e:
            print("fail",d["daft_link"])
