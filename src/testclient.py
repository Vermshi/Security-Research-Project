#!/usr/bin/env python

import time
import platform
from zapv2 import ZAPv2
from subprocess import Popen, PIPE, STDOUT
from testsuite import Test

class TestClient(object):

    def __init__(self, zapPort='7577'):
        print("Initiate")
        self.os = platform.system()
        self.zapPort = zapPort
        # TODO: Generate key
        self.zapApiKey = '123'
        self.zapStart()
        self.zapConfigure()
        self.tests = self.generateTestList()

    def runAllTests(self):
        print("Running tests")
        # Reset ZAP alerts
        if len(self.zap.core.alerts()) > 0:
            self.zap.core.new_session()
        # Start by disabling all scanners and add them later
        self.zap.ascan.disable_all_scanners()
        self.zap.pscan.disable_all_scanners()

        for test in self.tests:
            if test.engine == 'ZAP':
                if test.mode == 'passive':
                    self.zap.pscan.enable_scanners(test.testid)
                elif test.mode == 'active':
                    self.zap.ascan.enable_scanners(test.testid)

        self.zapRunSpider()

        for alert in self.zap.core.alerts():
            print("")
            print("---ALERT---")
            print(alert["description"])
            print("")
            print("---------------------------------------------------")
        
    # TODO: Come up with a better solution
    def generateTestList(self):
        tests = []
        tests.append(Test('SQL Injection', 40018, 'SQL injection may be possible.', 'ZAP', 'active', True, False))
        tests.append(Test('X-Frame-Options Header Scanner', 10020, 'X-Frame-Options header is not included in the HTTP response to protect against \'ClickJacking\' attacks.', 'ZAP', 'passive', True, False))
        tests.append(Test('Cookie No HttpOnly Flag', '10010', 'A cookie has been set without the HttpOnly flag, which means that the cookie can be accessed by JavaScript. If a malicious script can be run on this page then the cookie will be accessible and can be transmitted to another site. If this is a session cookie then session hijacking may be possible.', 'ZAP', 'passive', True, False))
        tests.append(Test('Web Browser XSS Protection Not Enabled', 10016, 'Web Browser XSS Protection is not enabled, or is disabled by the configuration of the \'X-XSS-Protection\' HTTP response header on the web server', 'ZAP', 'passive', True, False))
        tests.append(Test('Application Error Disclosure', '90022', "DESCRIPTION", 'ZAP', 'passive', True, True))
        return tests

    # Start the Zed Attack Proxy attack engine
    def zapStart(self):
    
        if self.os == 'Linux':
             startZap = Popen(["zap", "-port", self.zapPort, "-config", ("api.key="+self.zapApiKey)] , stdout=PIPE, stderr=STDOUT)
             # startZap.communicate()
             return

        elif self.os == 'Windows':
            # TODO:
            print("Windows not implemented yet")
            print("Start Zap proxy manually")
        else:
            print("OS not supported yet:" + self.os)

    # Configure Zed Attack Proxy
    def zapConfigure(self):
        print("configure zap")
        self.zap = ZAPv2(apikey=self.zapApiKey, proxies={'http': 'http://127.0.0.1:' + self.zapPort, 'https': 'http://127.0.0.1:' + self.zapPort}) 
        # TODO: The second port should eventually be a https port

    # Login to the target to test an authenticated session
    def zapCreateSession(self):
        # TODO: Use zap to start a session with the target
        return

    # Run all ZAP tests
    def zapRunAllTests(self):
        # do stuff
        print('Accessing target %s' % target)
        # try have a unique enough session...
        zap.urlopen(target)
        # Give the sites tree a chance to get updated
        time.sleep(2)

    def zapRunSpider(self):
        self.zap.urlopen(self.target)
        scanid = self.zap.spider.scan(self.target)
        # Give the Spider a chance to start
        time.sleep(2)
        while (int(self.zap.spider.status(scanid)) < 100):
            print('Spider progress %: ' + self.zap.spider.status(scanid))
        
    # Run single test from ZAP
    def zapRunSingleTest(self, testid):
        return

    # Set target to test
    def setTarget(self, target):
        self.target = target

    # Set the port number for zap
    def setZapPort(self, port):
        self.zapPort = port




