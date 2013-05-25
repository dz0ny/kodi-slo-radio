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
if req.status_code is 200:
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

print "Število postaj: %d" % len(za_izvoz)

# native

try:
    pstat = open('stations.pickle', 'w')
    pickle.dump(za_izvoz, pstat)
except Exception, e:
    print e

# json

try:
    jstat = codecs.open('stations.json', 'w', 'utf-8')
    json.dump(za_izvoz, jstat, sort_keys=True, indent=2)
    jstat.close()
except Exception, e:
    print e

# m3u

mstat = codecs.open('stations.m3u', 'w', 'utf-8')
print >> mstat, '#EXTM3U'
for x in za_izvoz:
    try:
        print >> mstat, '#EXTINF:' + x['name']
        print >> mstat, x['url'] + '\n'
    except Exception, e:
        print e

mstat.close()

# lame print json.dumps(stations, sort_keys=True, indent=2)
