#!/usr/bin/env python

import time
import platform
from zapv2 import ZAPv2
from subprocess import Popen


class testClient(object):

    os = ""
    zapPort = "7070"
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

    # Configure Zed Attack Proxy
    def zapConfigure(self):
        zap = ZAPv2(apikey=self.apikey, proxies={'http': 'http://127.0.0.1:' + self.zapPort, 'https': 'http://127.0.0.1:' + self.port})

    # Login to the target to test an authenticated session
    def zapCreateSession(self):
        # TODO: Use zap to start a session with the target
        return

    # Run all ZAP tests
    def zapRunAllTests(self):
        # do stuff
        print 'Accessing target %s' % target
        # try have a unique enough session...
        zap.urlopen(target)
        # Give the sites tree a chance to get updated
        time.sleep(2)

    # Run single test from ZAP
    def zapRunSingleTest(self, testid):
        return

    # Set target to test
    def setTarget(target):
        self.target = target

    # Set the port number for zap
    def setZapPort(port):
        self.zapPort = port
