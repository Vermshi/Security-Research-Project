#!/usr/bin/env python

from testsuite import TestSuite, Test
from subprocess import Popen, PIPE, STDOUT
import os
from zapv2 import ZAPv2
import time

class ZapTestSuite(TestSuite):

    zap = None
    api_key = None

    def start(self):
        #self.api_key = 123
        self.api_key = os.urandom(16)
        if self.os == 'Linux':
             Popen(["zap", "-port", self.http_port, "-config", ("api.key="+str(self.api_key))] )

        else:
            print("OS not supported yet:" + self.os)
            print("Start Zap proxy manually")
            print("Go to Tools -> Options -> API and change port to", self.http_port, "and API key to", self.api_key)

    def configure(self):
        self.zap = ZAPv2(apikey=str(self.api_key), proxies={'http': self.url + ':' + self.http_port,
                                                            'https': self.url + ':' + self.https_port})

    # def createsession(self):
    #     It is recommended to implement sessions to the test suite
    #

    def run_tests(self, targetURL):
        self.zap.urlopen(targetURL)

        self.zap.ascan.disable_all_scanners()
        self.zap.pscan.disable_all_scanners()
        for test in self.tests:
            if test.mode == 'passive' and test.enabled is True:
                self.zap.pscan.enable_scanners(test.testid)
            elif test.mode == 'active' and test.enabled is True:
                self.zap.ascan.enable_scanners(test.testid)

        # RUN PASSIVE TESTS
        scanid = self.zap.spider.scan(targetURL)
        time.sleep(2)
        while (int(self.zap.spider.status(scanid)) < 100):
            print('Spider progress %: ' + self.zap.spider.status(scanid))
        time.sleep(2)

        # Run ACTIVE TESTS
        scanid = self.zap.ascan.scan(targetURL)
        while int(self.zap.ascan.status(scanid)) < 100:
            print('Scan progress %: ' + self.zap.ascan.status(scanid))
            time.sleep(5)

        # Store the test results back into the tests list
        for index in range(len(self.tests)):
            for alert in self.zap.core.alerts():
                if self.tests[index].testid == int(alert['pluginId']):
                #if self.tests[index].name == alert['name']:
                    self.tests[index].description = alert['description']
                    self.tests[index].passed = False
                else:
                    self.tests[index].passed = True
        print("results?", self.zap.core.alerts())
        print("")
        return self.tests

    def generate_test_list(self):
        tests = []
        for scan in self.zap.pscan.scanners:
            tests.append(Test(scan['name'], scan['id'], None, self.engine_name, "UNKNOWN", "passive", None, True))

        for scan in self.zap.ascan.scanners():
            tests.append(Test(scan['name'], scan['id'], None, self.engine_name, "UNKNOWN", "active", None, True))

        return tests

    def import_policy(self, path, name):
        print("need to support importing policy from path")