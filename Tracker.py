#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twisted.web.server import Site
from twisted.web.resource import Resource

import platform
if platform.system() == 'Windows':
    from twisted.internet import iocpreactor
    try:
        #http://sourceforge.net/projects/pywin32/
        iocpreactor.install()
    except:
        pass
else:
    from twisted.internet import epollreactor
    try:
        epollreactor.install()
    except:
        pass

from twisted.internet import reactor

import logging
logging.basicConfig(level=logging.DEBUG)

import Config

from Announce import Announce
from Status import Status
from Dump import Dump
from Static import Static
from Scrape import Scrape

root = Resource()
root.putChild("announce", Announce())
root.putChild("scrape", Scrape())
root.putChild("status", Status())
root.putChild("dump", Dump())
root.putChild("", Static())

factory = Site(root, timeout = 30)
reactor.listenTCP(Config.LISTEN_PORT, factory)
reactor.run()
