#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twisted.web.resource import Resource

import json
from HashTableNew import HashTable

class Dump(Resource):
    isLeaf = True

    def render_GET(self, request):
        if request.uri == '/dump/save':
            dic = {}
            for info_hash in HashTable.dict_info_hash_completed:
                hash = ''
                for i in info_hash:
                    hash += hex(ord(i))[2:].zfill(2).upper()
                dic.update({hash:HashTable.dict_info_hash_completed[info_hash]})
            ret = json.dumps(dic)
            open('dump.txt', 'w').write(ret)
            return 'torrents %d completed has been save' % len(dic)
        elif request.uri == '/dump/load':
            js = json.loads(open('dump.txt', 'r').read())
            for info_hash in js:
                n = str()
                for i in range(0, 40, 2):
                    n += str(chr(int(info_hash[i:i+2], 16)))
                HashTable.dict_info_hash_completed[n] = js[info_hash]
            return 'torrents %d completed has been load' % len(js)