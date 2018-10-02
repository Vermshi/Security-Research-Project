#!/usr/bin/env python

import time
import platform
from zapv2 import ZAPv2
from subprocess import Popen


class testClient(object):

    os = ""
    zapport = "7070"
    # TODO: Generate secure api key
    zapApiKey = "123"

    def __init__(self):
        print "Initiate"
        self.os = platform.system()
        self.startZap()

# Start the Zed Attack Proxy attack engine
    def zapStart(self):

        if self.os == 'Linux':
             Popen(["zap", "-daemon", "-config", "api.key=", self.zapApiKey])
             return

        elif self.os == 'Windows':
            print "Windows not implemented yet"

        else:
            print "unknown os" + self.os

    def zapConfigure(self):
        zap = ZAPv2(apikey=self.apikey, proxies={'http': 'http://127.0.0.1:' + self.zapport, 'https': 'http://127.0.0.1:' + self.port})

    def zapTest(self):
        # do stuff
        print 'Accessing target %s' % target
        # try have a unique enough session...
        zap.urlopen(target)
        # Give the sites tree a chance to get updated
        time.sleep(2)

    def setTarget(target):
        self.target = target

    def setPort(port):
        self.zapport = port
