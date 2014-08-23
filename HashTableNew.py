#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Peer
import time
import Config
import logging

class HashTable:
    dict_by_info_hash = {}
    dict_info_hash_completed = {}

    last_cleanup_time = time.time()
    @staticmethod
    def find_peers_by_info_hash(info_hash):
        if info_hash in HashTable.dict_by_info_hash:
            return HashTable.dict_by_info_hash[info_hash]
        else:
            return {}

    @staticmethod
    def find_peer_by_peer_id_and_info_hash(peer_id, info_hash):
        peers = HashTable.find_peers_by_info_hash(info_hash)
        if peer_id in peers:
            return peers[peer_id]

    @staticmethod
    def remove_peer_by_peer_id_and_info_hash(peer_id, info_hash):
        peers = HashTable.find_peers_by_info_hash(info_hash)
        if peer_id in peers:
            peers.pop(peer_id)

    @staticmethod
    def update_peer_by_peer_id_and_info_hash(peer_id, info_hash):
        peers = HashTable.find_peers_by_info_hash(info_hash)
        if peer_id in peers:
            return peers[peer_id]

        p = Peer.Peer()
        if info_hash in HashTable.dict_by_info_hash:
            HashTable.dict_by_info_hash[info_hash].update({peer_id: p})
        else:
            HashTable.dict_by_info_hash[info_hash] = {peer_id: p}

        return p

    @staticmethod
    def do_clean_up():
        if time.time() - HashTable.last_cleanup_time > Config.CLEANUP_TIME:
            start = time.clock()
            cleanup_time_before = time.time() - Config.CLEANUP_TIME_OUT
            for info_hash in HashTable.dict_by_info_hash:
                for peer_id in HashTable.dict_by_info_hash[info_hash].keys():
                    if HashTable.dict_by_info_hash[info_hash][peer_id].last_keep_time < cleanup_time_before:
                        HashTable.dict_by_info_hash[info_hash].pop(peer_id)
            end = time.clock()
            Config.cleanup_time_query_at = end-start
            logging.debug('cleanup done... at:%lf' % (end-start))

    @staticmethod
    def get_torrent_count():
        return len(HashTable.dict_by_info_hash)

    @staticmethod
    def get_torrent_leechers_count(info_hash):
        peers = HashTable.find_peers_by_info_hash(info_hash)
        n = 0
        for peer in peers:
            if peers[peer].is_completed:
                n += 1
        return n

    @staticmethod
    def get_torrent_peers_count(info_hash):
        return len(HashTable.find_peers_by_info_hash(info_hash))

    @staticmethod
    def get_peer_count():
        #start = time.clock()
        n = 0
        for info_hash in HashTable.dict_by_info_hash:
            n += len(HashTable.dict_by_info_hash[info_hash])
        #end = time.clock()
        #logging.debug('get_peer_count done... at:%lf' % (end-start))
        return n

    @staticmethod
    def do_insert_test():
        for i in range(0,10000):
            for j in range(0,100):
                if i not in HashTable.dict_by_info_hash:
                    HashTable.dict_by_info_hash[i] = {}
                p = Peer.Peer()
                p.last_keep_time = 0
                HashTable.dict_by_info_hash[i].update({j:p})

    @staticmethod
    def add_completed_by_info_hash(info_hash):
        if info_hash in HashTable.dict_info_hash_completed:
            HashTable.dict_info_hash_completed[info_hash] += 1
        else:
            HashTable.dict_info_hash_completed[info_hash] = 1

    @staticmethod
    def get_completed_by_info_hash(info_hash):
        if info_hash in HashTable.dict_info_hash_completed:
            return HashTable.dict_info_hash_completed[info_hash]
        return 0

def test():
    print 'op1'
    p = HashTable.update_peer_by_peer_id_and_info_hash('PEER0','HASH0')
    p.ip = '0.0.0.0'
    print HashTable.dict_by_info_hash
    print 'op1'
    p = HashTable.update_peer_by_peer_id_and_info_hash('PEER1','HASH1')
    p.ip = '1.1.1.1'
    print HashTable.dict_by_info_hash
    print 'op2'
    p = HashTable.update_peer_by_peer_id_and_info_hash('PEER1','HASH0')
    p = HashTable.update_peer_by_peer_id_and_info_hash('PEER0','HASH1')
    print '00' + str(HashTable.find_peer_by_peer_id_and_info_hash('PEER0','HASH0'))
    print HashTable.dict_by_info_hash
    print 'op3'
    HashTable.remove_peer_by_peer_id_and_info_hash('PEER0','HASH0')
    print HashTable.dict_by_info_hash
    print 'op4'
    HashTable.remove_peer_by_peer_id_and_info_hash('PEER1','HASH1')
    print HashTable.dict_by_info_hash
    print 'op5'
    HashTable.remove_peer_by_peer_id_and_info_hash('PEER0','HASH1')
    print HashTable.dict_by_info_hash
    print 'op6'
    HashTable.update_peer_by_peer_id_and_info_hash('PEER1','HASH0')
    print HashTable.dict_by_info_hash

#test()