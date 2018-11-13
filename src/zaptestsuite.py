#!/usr/bin/env python

from testsuite import TestSuite, Test
from subprocess import Popen, PIPE, STDOUT
import os
from zapv2 import ZAPv2
import time
import platform

class ZapTestSuite(TestSuite):


    zap = None
    api_key = None

    # Proxy default settings:
    proxy_address = '127.0.0.1'
    proxy_port = '7576'

    def start(self):
        osys = platform.system()
        self.api_key = os.urandom(16)

        if osys == 'Linux':
            p = Popen(["zap", "-daemon", "-port", self.proxy_port, "-config", ("api.key="+str(self.api_key))], stdout=PIPE, stderr=STDOUT)
            #p = Popen(["zap", "-port", self.proxy_port, "-config", ("api.key="+str(self.api_key))], stdout=PIPE, stderr=STDOUT)
            while "Started callback server" not in str(p.stdout.readline()):
                 print("ZAP is LOADING")
            print("ZAP done LOADING")
        
        elif osys == 'Windows':
            p = Popen([r"C:\Program Files\OWASP\Zed Attack Proxy\zap.bat", "-daemon", '-port', self.proxy_port, '-config', ("api.key="+str(self.api_key))], cwd=r"C:\Program Files\OWASP\Zed Attack Proxy", stdout=PIPE, stderr=STDOUT)
            # TODO: Write log to pipe and check if zap is done loading
            while "Started callback server" not in str(p.stdout.readline()):
                 print("ZAP is LOADING")
            print("ZAP done LOADING")
        
        else:
            print("OS not supported yet:" + osys)
            print("Start Zap proxy manually")
            print("Go to Tools -> Options -> API and change port to", self.http_port, "and API key to", self.api_key)

    def configure(self):
        self.zap = ZAPv2(apikey=str(self.api_key), proxies={'http': self.proxy_address + ':' + self.proxy_port,
                                                            'https': self.proxy_address + ':' + self.proxy_port})

    # def createsession(self):
    #     It is recommended to implement sessions to the test suite
    #

    def run_tests(self, tests, targetURL):
        self.zap.urlopen(targetURL)

        self.zap.ascan.disable_all_scanners()
        self.zap.pscan.disable_all_scanners()
        for test in tests:
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
        for index in range(len(tests)):
            tests[index].passed = None
            for alert in self.zap.core.alerts():
                if str(tests[index].testid) == str(alert['pluginId']):
                #if self.tests[index].name == alert['name']:
                    tests[index].description = alert['description']
                    tests[index].passed = False
                
            if tests[index].passed != False and self.tests[index].enabled == True:
                tests[index].passed = True
        print("results?", self.zap.core.alerts())
        print("")
        return tests

    def generate_test_list(self):
        tests = []
        for scan in self.zap.pscan.scanners:
            tests.append(Test(scan['name'], scan['id'], None, self.engine_name, "UNKNOWN", "passive", None, True))

        for scan in self.zap.ascan.scanners():
            tests.append(Test(scan['name'], scan['id'], None, self.engine_name, "UNKNOWN", "active", None, True))

        return tests

    def import_policy(self, path, name):
        print("need to support importing policy from path")
