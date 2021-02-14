#!/usr/bin/python3
# -*- encoding: utf-8 -*-

"""Nova EPG parser, add mapping to CHANELS"""

from __future__ import print_function
from xml.sax.saxutils import escape
import datetime
import re
import requests


def _channel(channel, name):
    """Channel Id and Name"""
    print('  <channel id="{}">'.format(channel))
    print('    <display-name lang="el">{}</display-name>'.format(escape(name)))
    print('  </channel>')


def _programme(start, channel, title, desc):
    """Channel Programm using only start, end should be calculated"""
    print('  <programme start="{} +0200" channel="{}">'.format(start, channel))
    print('    <title lang="el">{}</title>'.format(escape(title)))
    print('    <desc>{}</desc>'.format(escape(desc)))
    print('  </programme>')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Referer': 'https://www.nova.gr/guide/',
}

CHANNELS = {
    '81': ('nova.insighttv.gr', 'InsightTV'),
    '221': ('nova.myzen.gr', 'MyZen'),
    '584': ('nova.one.gr', 'One'),
    '627': ('nova.eurosport1.gr', 'Eurosport1'),
    '638': ('nova.eurosport2.gr', 'Eurosport2'),
}

SDAY = datetime.date.today().strftime('%Y%m%d')
EDAY = (datetime.date.today() + datetime.timedelta(days=7)).strftime('%Y%m%d')
EPG_URL = 'https://www.nova.gr/api/v1/tvprogram/from/%s/to/%s' % (SDAY, EDAY)

# get epg
RES = requests.get(EPG_URL, headers=HEADERS)
JS = RES.json()

for cn, ci in set(sorted([(x['channelName'], x['ChannelId']) for x in JS['nodes']])):
    nci = CHANNELS.get(ci, None)
    if nci:
        _channel(nci[0], nci[1])

for x in JS['nodes']:
    nci = CHANNELS.get(x['ChannelId'], None)
    if not nci:
        continue
    s = ''.join(re.split('-| |:', x['datetime']))
    _programme(s, nci[0], x['title'], x['description'])
