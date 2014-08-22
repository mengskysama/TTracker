#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

class Peer():

    def __init__(self):
        self.socketip = None
        self.ip = None
        self.ipv6ip = None
        self.port = None
        #self.peer_id = None
        #self.info_hash = None
        self.downloaded_first = self.downloaded = None
        self.uploaded_first = self.uploaded = None
        self.left_first = self.left = None
        self.event = None
        self.last_keep_time = None
        self.is_completed = False
        #self.passkey = None

    def update(self, socketip, ip, ipv6ip, port, peer_id, info_hash, downloaded, uploaded, left, event, passkey=None):
        self.socketip = socketip
        self.ip = ip
        self.ipv6ip = ipv6ip
        self.port = port
        #self.peer_id = peer_id
        #self.info_hash = info_hash
        self.downloaded = downloaded
        self.uploaded = uploaded
        self.left = left
        if left == 0:
            self.is_completed = True
        self.event = event
        self.last_keep_time = time.time()
        #self.passkey = passkey