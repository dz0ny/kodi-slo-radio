#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
from pyquery import PyQuery
import pickle
import codecs


def izberi_http(text):
    urls = text.split("\n")
    # for url in urls:
    #     if url.find("http") != -1:
    #         return url
    return urls[0]

za_izvoz = []
lame = set()

za_izvoz.append({
    'name': "Radio Terminal",
    'label': "Urbani radio",
    'img': "http://d1i6vahw24eb07.cloudfront.net/s164797q.png",
    'id': "1",
    'bitrate': "192",
    'url': "http://live.radioterminal.si",
})

req = requests.get("http://opml.radiotime.com/Browse.ashx?id=r100411")
if req.status_code == 200:
    page = PyQuery(req.text.encode("utf-8"))
    for link in page("outline"):

        if "station" == link.get("item"):
            stream = requests.get(link.get("URL"))
            url = izberi_http(stream.text)
            postaja = {
                'name': link.get("text"),
                'label': link.get("subtext"),
                'img': link.get("image"),
                'id': link.get("preset_id"),
                'bitrate': link.get("bitrate"),
                'url': url,
            }
            if url not in lame:
                lame.add(url)
                za_izvoz.append(postaja)


za_izvoz.sort(key=lambda postaja: postaja['name'])

print(f"Število postaj: {len(za_izvoz)}")

# native

try:
    pstat = open('stations.pickle', 'w')
    pickle.dump(za_izvoz, pstat)
except Exception as e:
    print(e)

# json

try:
    jstat = open("stations.json", "w")
    data = json.dumps(za_izvoz, sort_keys=True, indent=2)
    print(data)
    jstat.write(data)
    jstat.close()
except Exception as e:
    print(e)


# lame print json.dumps(stations, sort_keys=True, indent=2)
