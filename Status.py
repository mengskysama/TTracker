#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twisted.web.resource import Resource

from HashTableNew import HashTable
import json

import Config

class Status(Resource):
    isLeaf = True

    def render_GET(self, request):
        list = {}
        list.update({'torrent_count':HashTable.get_torrent_count()})
        list.update({'peers_count':HashTable.get_peer_count()})
        list.update({'process_announce_query_at':'%lf' % Config.process_announce_query_at})
        list.update({'process_scrape_query_at':'%lf' % Config.process_scrape_query_at})

        return json.dumps(list)

