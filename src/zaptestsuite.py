#!/usr/bin/env python

from testsuite import TestSuite, Test
from subprocess import Popen, PIPE, STDOUT
import os
from zapv2 import ZAPv2


class ZapTestSuite(TestSuite):

    zap = None
    api_key = None

    def start(self):
        self.api_key = os.urandom(16)
        if self.os == 'Linux':
             Popen(["zap", "-port", self.http_port, "-config", ("api.key="+str(self.api_key))] )

        else:
            print("OS not supported yet:" + self.os)
            print("Start Zap proxy manually")


    def configure(self):
        self.zap = ZAPv2(apikey=str(self.api_key), proxies={'http': self.url + ':' + self.http_port,
                                                       'https': self.url + ':' + self.https_port})

    # def createsession(self):
    #     It is recommended to implement sessions to the test suite
    #

    def run_tests(self, targetURL):
        self.zap.urlopen(targetURL)
        self.run_passive_tests(targetURL)

    def run_active_tests(self):
        print("need to support running of active tests")

    def run_passive_tests(self, targetURL):
        scanid = self.zap.spider.scan(targetURL)
        while (int(self.zap.spider.status(scanid)) < 100):
            print('Spider progress %: ' + self.zap.spider.status(scanid))

    def generate_test_list(self):
        tests = []
        for scan in self.zap.pscan.scanners:
            tests.append(Test(scan['name'], scan['id'], None, self.engine_name, "UNKNOWN", "passive", False, True))

        for scan in self.zap.ascan.scanners:
            tests.append(Test(scan['name'], scan['id'], None, self.engine_name, "UNKNOWN", "passive", False, True))

        return tests

    def import_policy(self, path, name):
        print("need to support importing policy from path")