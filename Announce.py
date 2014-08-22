#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twisted.web.resource import Resource
from twisted.internet import address

import bencode
import HashTableNew
import time
import random
import logging

import Config
from HashTableNew import HashTable

def bencode_faild_str(str):
    return bencode.bencode({'failure reason':str})

class Announce(Resource):
    isLeaf = True

    def GeneratePeerListNew(self, peers, numwant, ret_ipv6):
        #get random pees
        #force no compact
        if len(peers) <= numwant:
            peers = list(peers.values())
        else:
            peers = random.sample(peers.values(), numwant)

        peerslst = []
        for p in peers:
            if p.socketip is not None:
                peer = {"ip": p.socketip, "port": p.port}
                peerslst.append(peer)
            if ret_ipv6 and p.ipv6ip is not None:
                peer = {"ip": p.ipv6ip, "port": p.ipv6port}
                peerslst.append(peer)
        return peerslst

    def str2int(self, str):
        try:
            ret = int(str)
            if ret >= 0:
                return ret
            return None
        except:
            return None

    def str2long(self, str):
        try:
            ret = long(str)
            if ret >= 0l:
                return ret
            return None
        except:
            return None

    def get_argument(self, request, key, default = None):
        if key in request.args:
            return request.args[key][0]
        else:
            return default

    def render_GET(self, request):

        HashTableNew.HashTable.do_clean_up()

        start = time.clock()

        #ipv6ip = None
        client = request.client

        if isinstance(client, address.IPv4Address):
            socketIp = client.host
        #notice if use ipv6 couldn't get real ipv4 ip
        #elif isinstance(client, address.IPv6Address):
        #    ipv6ip = client.host

        #if ipv6ip is None:
        ipv6ip      = self.get_argument(request, 'ipv6')

        ip          = self.get_argument(request, 'ip')
        info_hash   = self.get_argument(request, 'info_hash')
        peer_id     = self.get_argument(request, 'peer_id')
        key         = self.get_argument(request, 'key')
        port        = self.get_argument(request, 'port')
        ipv6port    = None
        downloaded  = self.get_argument(request, 'downloaded', 0)
        uploaded    = self.get_argument(request, 'uploaded', 0)
        left        = self.get_argument(request, 'left', 0)
        passkey     = self.get_argument(request, 'passkey')
        event       = self.get_argument(request, 'event', '')
        numwant     = self.get_argument(request, 'numwant', 50)

        if Config.PRIVETE_TRACKER:
            if passkey is None:
                return bencode_faild_str('Missing passkey')

        #check argments
        if info_hash is None:
            return bencode_faild_str('Missing info_hash')
        if len(info_hash) != 20:
            return bencode_faild_str('Valid info_hash')
        if peer_id is None:
            return bencode_faild_str('Missing peer_id')
        if len(peer_id) != 20:
            return bencode_faild_str('Valid peer_id')
        if port is None:
            return bencode_faild_str('Missing port')
        if len(port) > 5:
            return bencode_faild_str('Valid port')
        if ip is not None and len(ip) > 15:
            return bencode_faild_str('Valid ip')
        if ipv6ip is not None and len(ipv6ip) > 47:
            return bencode_faild_str('Valid ipv6ip')

        downloaded = self.str2long(downloaded)
        uploaded = self.str2long(uploaded)
        left = self.str2long(left)
        numwant = self.str2int(numwant)

        if downloaded is None:
            return bencode_faild_str('Missing downloaded')
        if uploaded is None:
            return bencode_faild_str('Missing uploaded')
        if left is None:
            return bencode_faild_str('Missing left')
        if numwant is None:
            return bencode_faild_str('Valid numwant')

        if numwant > 100:
            numwant = 100

        #bep_0007
        if ipv6ip is not None:
            if ipv6ip[0] == '[':
                pos = ipv6ip.find(']:')
                if pos != -1:
                    #[::]:0
                    ipv6port = ipv6port[pos+2]
                    ipv6ip = ipv6ip[0:pos+1]
                else:
                    #[::]
                    ipv6ip = port
            else:
                ipv6ip = '[' + ipv6ip + ']'
                ipv6port = port

        ret_ipv6 = False
        if ipv6ip is not None:
            if ipv6ip[1:6].lower() != 'fe80:':
                ret_ipv6 = True
        if socketIp is None:
            #ipv6 socket
            ret_ipv6 = True

        if event is None or event == '':
            #some client event=&
            p = HashTable.update_peer_by_peer_id_and_info_hash(peer_id, info_hash)
            p.update(socketIp, ip, ipv6ip, port, peer_id, info_hash, downloaded, uploaded, left, event, passkey)
        if event == 'completed':
            p = HashTable.find_peer_by_peer_id_and_info_hash(peer_id, info_hash)
            HashTable.add_completed_by_info_hash(info_hash)
            p = HashTable.update_peer_by_peer_id_and_info_hash(peer_id, info_hash)
            p.update(socketIp, ip, ipv6ip, port, peer_id, info_hash, downloaded, uploaded, left, event, passkey)
        if event == 'started':
            #pt need process something else
            p = HashTable.update_peer_by_peer_id_and_info_hash(peer_id, info_hash)
            p.update(socketIp, ip, ipv6ip, port, peer_id, info_hash, downloaded, uploaded, left, event, passkey)
            p.uploaded_first = uploaded
            p.downloaded_first = downloaded
            p.left_first = left
        elif event == 'stopped':
            HashTable.remove_peer_by_peer_id_and_info_hash(peer_id, info_hash)

        if event == 'stopped':
            peers = []
        else:
            peers = HashTable.find_peers_by_info_hash(info_hash)
            peers = self.GeneratePeerListNew(peers, numwant, ret_ipv6)

        peers_cnt = HashTable.get_torrent_peers_count(info_hash)
        leechers_cnt = HashTable.get_torrent_peers_count(info_hash)
        seeders_cnt = peers_cnt - leechers_cnt

        ret = {
            "interval":     1800,
            "min_interval": 15,
            "complete":     seeders_cnt,
            "incomplete":   leechers_cnt,
            "peers":        peers,
            }

        ret = bencode.bencode(ret)
        end = time.clock()
        logging.debug('process query at:%lf' % (end-start))
        Config.process_announce_query_at = end-start
        return ret

