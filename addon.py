#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2012 dz0ny
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from xbmcswift import Plugin, download_page
from xbmcswift.ext.playlist import playlist
import os
import utils
try:
    import json
except ImportError:
    import simplejson as json
from xbmcswift import xbmc, xbmcgui

__plugin__ = 'Slovenske radijske postaje'
__plugin_id__ = 'plugin.audio.radio-slovenija'
__addoninfo__ = utils.get_addoninfo(__plugin_id__)

plugin = Plugin(__plugin__, __plugin_id__, __file__)

plugin.register_module(playlist, url_prefix='/_playlist')


def get_streams():
    filename = os.path.join(__addoninfo__['path'], 'resources', 'stations.json')
    src = open(filename, 'r')
    try:
        resp = json.load(src)
    finally:
        src.close()

    # Return a JSON list of the streams

    return resp


#### Plugin Views ####

# Default View

@plugin.route('/', default=True)
def show_homepage():
    Streams = get_streams()
    items = []
    for station in Streams:
        try:
            items.append({
                'label': station['name'],
                'label2': station['label'],
                'url': plugin.url_for('startplay', URLStream=station['url'], Name=station['name'],
                                      Icon=station['img']),
                'thumbnail': station['img'],
                })
        except Exception, e:
            print e
            print station

    return plugin.add_items(items)


@plugin.route('/live/<Name>/<URLStream>/<Icon>')
def startplay(URLStream, Name, Icon):
    rtmpurl = URLStream
    Thumb = Icon
    li = xbmcgui.ListItem(Name, Name, Thumb, Thumb)
    li.setInfo('music', {'Title': Name})
    xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(rtmpurl, li)

    # Return an empty list so we can test with plugin.crawl() and plugin.interactive()

    return []

if __name__ == '__main__':
    plugin.run()
