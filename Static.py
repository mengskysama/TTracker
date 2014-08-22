#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twisted.web.resource import Resource

import HashTableNew
import json

import Config

class Static(Resource):
    isLeaf = True

    def render_GET(self, request):
        return open('index.htm', 'r').read()