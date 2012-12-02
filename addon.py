#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc
from xbmcswift2 import Plugin, ListItem
import xbmcaddon
import os
import pickle
import xbmc
import xbmcgui

plugin = Plugin()


def get_stations():
    filename = os.path.join(xbmcaddon.Addon(plugin.id).getAddonInfo('path'), 'resources',
                            'stations.pickle')
    src = open(filename, 'r')
    try:
        streams = pickle.load(src)
    finally:
        src.close()

    return streams


postaje = get_stations()


@plugin.route('/')
def index():
    items = []
    for station in postaje:
        try:
            items.append({
                'label': station['name'],
                'label2': station['label'],
                'info': {'title': station['name'], 'size': int(station['bitrate'])},
                'path': plugin.url_for('startplay', id=station['url']),
                'icon': station['img'],
                'thumbnail': station['img'],
                'is_playable': False,
                'info_type': 'music',
                })
        except Exception, e:
            print e
            print station

    finish_kwargs = {'sort_methods': [('TITLE', '%X'), ('SIZE', '%X')]}

    return plugin.finish(items, **finish_kwargs)


@plugin.route('/live/<id>')
def startplay(id):
    station = filter(lambda x: x['url'] == id, postaje)[0]
    li = xbmcgui.ListItem(station['name'], station['name'], station['img'], station['img'])
    li.setInfo('music', {'Title': station['name']})
    xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(station['url'], li)
    item = [{
        'label': station['name'],
        'label2': station['label'],
        'info': {'title': station['name'], 'size': int(station['bitrate'])},
        'path': plugin.url_for('startplay', id=station['url']),
        'icon': station['img'],
        'thumbnail': station['img'],
        'is_playable': True,
        'selected': True,
        'info_type': 'music',
        }]
    return item

if __name__ == '__main__':
    plugin.run()
