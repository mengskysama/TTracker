#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twisted.web.resource import Resource

import bencode
import HashTableNew
import time
import logging

import Config
from HashTableNew import HashTable

def bencode_faild_str(str):
    return bencode.bencode({'failure reason':str})

class Scrape(Resource):
    isLeaf = True

    def render_GET(self, request):

        HashTableNew.HashTable.do_clean_up()

        start = time.clock()

        info_hash_lst = []
        if 'info_hash' in request.args:
            info_hash_lst = request.args['info_hash']
        else:
            return bencode_faild_str('Mising info_hash')

        ret = {}
        for info_hash in info_hash_lst:
            peers_cnt = HashTable.get_torrent_peers_count(info_hash)
            seeders_cnt = HashTable.get_torrent_seeders_count(info_hash)
            leechers_cnt = peers_cnt - seeders_cnt
            completed_cnt = HashTable.get_completed_by_info_hash(info_hash)
            info_table = {"complete": seeders_cnt, "downloaded": completed_cnt, "incomplete": leechers_cnt}
            ret.update({info_hash:info_table})

        ret = {'files': ret}
        ret = bencode.bencode(ret)
        end = time.clock()
        logging.debug('process scrape query at:%lf' % (end-start))
        Config.process_scrape_query_at = end-start
        return ret