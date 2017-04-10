# -*- coding: utf-8 -*-

import routing
import logging
import xbmcaddon
from resources.lib import kodiutils
from resources.lib import kodilogging
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory
import os
import pickle


ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))
kodilogging.config()
plugin = routing.Plugin()


def get_stations():
    filename = os.path.join(
        xbmcaddon.Addon(plugin.id).getAddonInfo('path'), 'resources',
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
            addDirectoryItem(plugin.handle, plugin.url_for(startplay, station['url']), station['name'], True)
        except Exception, e:
            print e
            print station

    
    endOfDirectory(plugin.handle)


@plugin.route('/live/<id>')
def startplay(id):
    station = filter(lambda x: x['url'] == id, postaje)[0]
    li = xbmcgui.ListItem(station['name'], station[
                          'name'], station['img'], station['img'])
    li.setInfo('music', {'Title': station['name']})
    xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(station['url'], li)

    addDirectoryItem(plugin.handle, "", station['name'])
    endOfDirectory(plugin.handle)

def run():
    plugin.run()
