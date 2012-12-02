#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import simplejson
import json
from pyquery import PyQuery
import pickle

urls = ['http://tunein.com/search/page/?id=r101900&page=true&filter=!p',
        'http://tunein.com/search/page/?id=r101901&page=true&filter=!p',
        'http://tunein.com/search/page/?id=r100411&page=true&filter=!p',
        'http://tunein.com/search/page/?query=radioterminal',
        'http://tunein.com/search/page/?id=r100411&page=true&filter=!p?other=true']
stations = []
t_stations = []
for url in urls:
    print 'REQ:', url
    req = requests.get(url)
    if req.status_code is 200:
        purl = req.json['PagingUrl']

        # poglej za nasledno stran

        if purl and purl not in urls:
            urls.append('http://tunein.com' + purl)

        # Dobi vse postaje na tej strani

        rlist = req.json['Results']
        for st in rlist:

            # print st['TitleSearch']

            if st['TitleSearch'] not in t_stations:
                stations.append({
                    'name': st['TitleSearch'],
                    'label': st['Subtitle'],
                    'img': st['SearchLogoUrl'],
                    'url': 'http://tunein.com' + st['Url'],
                    })
                t_stations.append(st['TitleSearch'])
            else:
                print 'skip: ', st['TitleSearch']

# id streamov

for station in stations:
    req = requests.get(station['url'])
    if req.status_code is 200:
        page = PyQuery(req.text)
        script = page('script')
        for data in script:
            src = data.text_content()
            if 'StreamUrl' in src:
                d_json = src[src.find('StationId') - 1:src.find('StreamSupport') - 4]
                if len(d_json):
                    ral_json = json.loads('{' + d_json + '}')
                    station['img'] = ral_json['Logo']
                    station['url'] = ral_json['StreamUrl']
                    station['name'] = station['name'].split(' - ')[0]

# get real ids

for station in stations:
    if len(station['url']) > 1:
        req = requests.get(station['url'])
        print station['url']

        if req.status_code is 200:
            data = req.text
            data = req.text[2:data.find('});') + 1]
            str_json = json.loads(data)
            station['url'] = str_json['Streams'][0]['Url']
        print

za_izvoz = []
for station in stations:
    if len(station['url']) > 0:
        za_izvoz.append(station)
    else:
        print 'skip ker nima url', station['name']

za_izvoz.sort(key=lambda postaja: postaja['name'])


jstat = open('stations.json', 'w')
simplejson.dump(za_izvoz, jstat, sort_keys=True, indent=2)
jstat.close()

m3u = '#EXTM3U\r\n'
mstat = open('stations.m3u', 'w')
for x in za_izvoz:
    try:
        print >> mstat, '#EXTINF:1,' + x['name']
        print >> mstat, x['url']
    except Exception, e:
        print e

mstat.close()

# lame print json.dumps(stations, sort_keys=True, indent=2)
