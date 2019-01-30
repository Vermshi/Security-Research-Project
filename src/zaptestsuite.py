#!/usr/bin/env python

from testsuite import TestSuite, Test
from subprocess import check_output, Popen, PIPE, STDOUT
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
    target_address = ""
    target_http_port = None
    target_https_port = None

    def start(self):
        """
        Start the ZAP engine in the background
        """

        osys = platform.system()
        api_key = os.urandom(16)
        proxy_address = '127.0.0.1'
        proxy_port = '7576'

        print("Start ZAP")

        if osys == 'Linux':

            print("Kill port")
            # Kill the proxy in case zap was not shutdown correctly
            kill_port(int(proxy_port))

            version = check_output(["cat", "/etc/os-release"]).decode("utf-8")
            wd = os.getcwd()
            if "Ubuntu" in version:
                os.chdir("/opt/zaproxy")
            else:
                os.chdir("/usr/share/owasp-zap")
            p = Popen(["java", "-jar", "zap-2.7.0.jar", "-dir", ".", "-daemon", "-port", proxy_port, "-config", ("api.key="+str(api_key))], stdout=PIPE, stderr=STDOUT)
            os.chdir(wd)
            #p = Popen(["zap", "-dir", ".", "-daemon", "-port", proxy_port, "-config", ("api.key="+str(api_key))], stdout=PIPE, stderr=STDOUT)
            #p = Popen(["zap", "-port", proxy_port, "-config", ("api.key="+str(api_key))], stdout=PIPE, stderr=STDOUT)
            readline = p.stdout.readline()
            print("Waiting for ZAP launch")
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
            print("Try using the docker image instead")
            return False

        self.zap = ZAPv2(apikey=str(api_key), proxies={'http': proxy_address + ':' + proxy_port,
                                                            'https': proxy_address + ':' + proxy_port})

        # Install addons

        # print(self.zap.autoupdate.marketplace_addons)

        # Install XSRF forgery supporting addon
        xsrf_addon = 'ascanrulesBeta'
        self.zap.autoupdate.install_addon(xsrf_addon)

        return True

    def connect(self, address, http_port=None, https_port=None):
        """
        Connect to the targetURL. ZAP can only connect to one target at the time, so this must be performed in the run
        function as well.
        """

        self.target_address = address

        if https_port and len(https_port) > 0:
            try:
                self.zap.urlopen("https://" + address + ":" + http_port)
                self.target_https_port = https_port
            except ConnectionError as e:
                print('Could not connect to', "https://" + address + ":" + http_port)
                print(e)
                return False

        if http_port and len(http_port) > 0:
            try:
                self.zap.urlopen("http://" + address + ":" + http_port)
                self.target_http_port = http_port
            except ConnectionError as e:
                print('Could not connect to', "http://" + address + ":" + http_port)
                print(e)
                return False

        return True

    def generate_test_list(self):
        """
        This function must make a array of Test objects representing each of the tests that can be executed by the engine.
        The list must be compatible for the run_tests function

        :return: List of Test objects
        :rtype: Array[Test...]
        """

        tests = []

        test_dictionary = self.get_tests_from_file("tests.csv", self.engine_name)

        for scan in self.zap.pscan.scanners:
            try:
                tests.append(Test(
                    name=scan['name'],
                    testid=scan['id'],
                    description="",
                    engine=self.engine_name,
                    vulnerability=test_dictionary[scan['name']][0],
                    mode="passive",
                    difficulty=test_dictionary[scan['name']][1],
                    passed=None,
                    enabled=(scan['enabled'] == 'true')
                ))
            # Continue to not crash the program because we did not store test in our tests.csv file
            except:
                print("Test <<", scan["name"], ">> not found in tests.csv file")
                continue

        for scan in self.zap.ascan.scanners():

            try:
                tests.append(Test(
                    name=scan['name'],
                    testid=scan['id'],
                    description="",
                    engine=self.engine_name,
                    vulnerability=test_dictionary[scan['name']][0],
                    mode="active",
                    difficulty=test_dictionary[scan['name']][1],
                    passed=None,
                    enabled=(scan['enabled'] == 'true')
            ))
            except:
                # print("Test", scan["name"], "not found in tests.csv file")
                continue

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
        #self.zap.ascan.set_option_default_policy(name)

        # TODO: Changes in the a scan policy will not be made once they have been set. How to fix that? ZAP does not support deletion of policies

        # Return the new test list
        return self.generate_test_list()

    def run_tests(self, tests):
        """
        Run all enabled tests against the target url. The Test objects within the tests array describes each test.
        The array should be changed according to how the outcome of the tests are and returned

        :param tests: Array of Test objects
        :type tests: Array[Test...]
        :return: Array of test objects
        :rtype: Array[Test...]
        """

        # Activate only enabled tests
        self.zap.ascan.disable_all_scanners()
        self.zap.pscan.disable_all_scanners()

        # TODO: Handle file import for policy. For this line many tests are missing in the xml file.
        #  Also the import doesnt always work?
        #  Most important is that this import sets strength and threshold

        self.import_policy("testpolicy.xml", "test_policy4")

        for test in tests:
            if test.mode == 'passive' and test.enabled is True:
                if test.enabled is True:
                    self.zap.pscan.enable_scanners(test.testid)
                else:
                    self.zap.pscan.disable_scanners(test.testid)
            elif test.mode == 'active':
                if test.enabled is True:
                    print("ENABLED", test.name, test.testid)
                    self.zap.ascan.enable_scanners(test.testid)
                    #self.zap.ascan.set_policy_attack_strength(test.testid, "HIGH")
                    #self.zap.ascan.set_policy_alert_threshold(test.testid, "OFF")
                else:
                    self.zap.ascan.disable_scanners(test.testid)
                    print("DISABLED", test.name)

        # TODO: Contains spaghetti code below?

        print("Policy")
        print(self.zap.ascan.policies())
        print("Default")
        print(self.zap.ascan.option_default_policy)
        print("passive scanners")
        for scan in self.zap.pscan.scanners:
            if scan["enabled"] == 'true':
                print(scan)
                print("")
        #print(self.zap.pscan.scanners)
        print("active scanners")
        for scan in self.zap.ascan.scanners():
            if scan["enabled"] == 'true':
                print(scan)
                print("")
        # Run tests on https port
        if self.target_https_port:
            self.zap.urlopen("https://" + self.target_address + ":" + self.target_https_port)

            # RUN PASSIVE TESTS
            print("Run Spider on port:", self.target_https_port)
            https_spider = self.zap.spider.scan("https://" + self.target_address + ":" + self.target_https_port)
            while (int(self.zap.spider.status(https_spider)) < 100):
                print('Spider progress %: ' + self.zap.spider.status(https_spider))
                time.sleep(0.1)
            # Give the passive tests a chance to finish
            time.sleep(4)

            # Run ACTIVE TESTS
            print("Run active scan on port:", self.target_https_port)
            https_scan = self.zap.ascan.scan("https://" + self.target_address + ":" + self.target_https_port)
            while int(self.zap.ascan.status(https_scan)) < 100:
                print('Scan progress %: ' + self.zap.ascan.status(https_scan))
                time.sleep(3)

        # Run tests on http port
        if self.target_http_port:
            self.zap.urlopen("http://" + self.target_address + ":" + self.target_http_port)

            # RUN PASSIVE TESTS
            print("Run Spider on port:", self.target_http_port)
            http_spider = self.zap.spider.scan("http://" + self.target_address + ":" + self.target_http_port)
            while (int(self.zap.spider.status(http_spider)) < 100):
                print('Spider progress %: ' + self.zap.spider.status(http_spider))
                time.sleep(0.1)
            # Give the passive tests a chance to finish
            time.sleep(4)

            # Run ACTIVE TESTS
            print("Run active scan on port:", self.target_http_port)
            http_scan = self.zap.ascan.scan("http://" + self.target_address + ":" + self.target_http_port)
            while int(self.zap.ascan.status(http_scan)) < 100:
                print('Scan progress %: ' + self.zap.ascan.status(http_scan))
                time.sleep(3)

        # Store the test results back into the tests list. In ZAP all tests ran on different targets are collected
        for index in range(len(tests)):
            tests[index].passed = None
            for alert in self.zap.core.alerts():
                if str(tests[index].testid) == str(alert['pluginId']):
                    tests[index].description = alert['description']
                    tests[index].passed = False

            # If the tests have not been classified as not passed they are by now passed
            if tests[index].passed is not False and tests[index].enabled is True:
                tests[index].passed = True
        return tests

    def shutdown(self):
        """
        Properly shut down the zap engine
        """
        self.zap.core.shutdown()
