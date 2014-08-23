#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twisted.web.resource import Resource

from HashTableNew import HashTable
import json

import Config

class Status(Resource):
    isLeaf = True

    def render_GET(self, request):
        lst = {}
        lst.update({'torrent_count': HashTable.get_torrent_count()})
        lst.update({'peers_count': HashTable.get_peer_count()})
        lst.update({'process_announce_query_at': float(Config.process_announce_query_at)})
        lst.update({'process_scrape_query_at': float(Config.process_scrape_query_at)})
        lst.update({'cleanup_time_query_at': float(Config.cleanup_time_query_at)})
        return json.dumps(lst)

