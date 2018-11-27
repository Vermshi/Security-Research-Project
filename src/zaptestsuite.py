#!/usr/bin/env python

from testsuite import TestSuite, Test
from subprocess import Popen, PIPE, STDOUT
import os
from zapv2 import ZAPv2
import time
import platform
from killport import kill_port


class ZapTestSuite(TestSuite):
    """
    Module to automate use of ZAP and its API
    """

    zap = None
    targetURL = ""

    def start(self):
        """
        Start the ZAP engine in the background
        """

        osys = platform.system()
        api_key = os.urandom(16)
        proxy_address = '127.0.0.1'
        proxy_port = '7576'

        # Kill the proxy in case
        kill_port(int(proxy_port))

        if osys == 'Linux':
            p = Popen(["zap", "-dir", ".", "-daemon", "-port", proxy_port, "-config", ("api.key="+str(api_key))], stdout=PIPE, stderr=STDOUT)
            #p = Popen(["zap", "-port", proxy_port, "-config", ("api.key="+str(api_key))], stdout=PIPE, stderr=STDOUT)
            readline = p.stdout.readline()
            while "ZAP is now listening" not in str(readline):
                readline = p.stdout.readline()
                continue
            print("ZAP is done loading")

        elif osys == 'Windows':
            p = Popen([r"C:\Program Files\OWASP\Zed Attack Proxy\zap.bat", '-daemon', '-port', proxy_port, '-config', ("api.key="+str(api_key))], cwd=r"C:\Program Files\OWASP\Zed Attack Proxy", stdout=PIPE, stderr=STDOUT)
            readline = p.stdout.readline()
            while "ZAP is now listening" not in str(readline):
                readline = p.stdout.readline()
                continue
            print("ZAP done LOADING")

        else:
            print("OS not supported yet:" + osys)
            print("Start Zap proxy manually")
            print("Go to Tools -> Options -> API and change port to", proxy_port, "and API key to", api_key)
            return False

        self.zap = ZAPv2(apikey=str(api_key), proxies={'http': proxy_address + ':' + proxy_port,
                                                            'https': proxy_address + ':' + proxy_port})
        return True

    def connect(self, address, http_port=None, https_port=None):
        """
        Connect to the targetURL
        """
        if(http_port):
            self.targetURL = "http://" + address + ":" + http_port
        # ZAP active scanner may not be able to run on https
        #elif(https_port):
        #    self.targetURL = address + ":" + http_port
        try:
            print(self.targetURL)
            self.zap.urlopen('http://' + self.targetURL)
            return True
        except:
            print('Could not connect to', self.targetURL)
            print('Specified URL must be on the format <address>:<port>')
            print("The URL was", self.targetURL)

            return False

    def generate_test_list(self):
        """
        This function must make a array of Test objects representing each of the tests that can be executed by the engine.
        The list must be compatible for the run_tests function

        :return: List of Test objects
        :rtype: Array[Test...]
        """

        tests = []
        for scan in self.zap.pscan.scanners:
            tests.append(Test(scan['name'], scan['id'], "", self.engine_name, "UNKNOWN", "passive", None, (scan['enabled'] == 'true')))

        for scan in self.zap.ascan.scanners():
            tests.append(Test(scan['name'], scan['id'], "", self.engine_name, "UNKNOWN", "active", None, (scan['enabled'] == 'true')))

        return tests

    def import_policy(self, file="testpolicy.xml", name="testpolicy"):
        """
        Import testing policy from file. This makes the initial configuration of which tests that are enabled.
        As well as other policies such as strength and sensitivity

        :param path: File path to config file
        :type path: str
        :param name: Policy name, may be useful for the engine
        :type name: str
        """

        # Find the absolute path as required by ZAP
        path = os.path.abspath(file)

        # Import and set a new attack scan policy
        self.zap.ascan.import_scan_policy(path)
        self.zap.ascan.set_option_attack_policy(name)
        self.zap.ascan.set_option_default_policy(name)

        # TODO: Changes in the a scan policy will not be made once they have been set. How to fix that? ZAP does not support deletion of policies

        # Return the new test list
        return self.generate_test_list()

    def run_tests(self, tests):
        """
        Run all enabled tests against the target url. The Test objects within the tests array describes each test.
        The array should be changed according to how the outcome of the tests are and returned

        :param tests: Array of Test objects
        :type tests: Array[Test...]
        :param targetURL: The target including address and port
        :type targetURL: str
        :return: Array of test objects
        :rtype: Array[Test...]
        """
        self.zap.ascan.disable_all_scanners()
        self.zap.pscan.disable_all_scanners()
        for test in tests:
            if test.mode == 'passive' and test.enabled is True:
                self.zap.pscan.enable_scanners(test.testid)
            elif test.mode == 'active' and test.enabled is True:
                self.zap.ascan.enable_scanners(test.testid)

        # RUN PASSIVE TESTS
        print("Run Spider")
        scanid = self.zap.spider.scan(self.targetURL)
        while (int(self.zap.spider.status(scanid)) < 100):
            print('Spider progress %: ' + self.zap.spider.status(scanid))
            time.sleep(0.1)
        # Give the passive scanner a chance to finish (IMPORTANT)
        time.sleep(3)

        # Run ACTIVE TESTS
        print("Run active scan")
        scanid = self.zap.ascan.scan(self.targetURL)
        while int(self.zap.ascan.status(scanid)) < 100:
            print('Scan progress %: ' + self.zap.ascan.status(scanid))
            time.sleep(5)

        # Store the test results back into the tests list
        for index in range(len(tests)):
            tests[index].passed = None
            for alert in self.zap.core.alerts():
                if str(tests[index].testid) == str(alert['pluginId']):
                    tests[index].description = alert['description']
                    tests[index].passed = False
                
            if tests[index].passed != False and tests[index].enabled == True:
                tests[index].passed = True
        return tests

    def shutdown(self):
        """
        Properly shut down the zap engine
        """
        self.zap.core.exit()
