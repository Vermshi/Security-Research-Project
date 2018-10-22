#!/usr/bin/env python

import warnings

class TestSuite(object):
    """This class is abstract. The required functions are:"""

    def __init__(self, engine_name='Custom Engine', http_proxy=None, https_proxy=None):
        print("Initiate Test Suite")
        self.engine_name = engine_name
        self.http_proxy = http_proxy
        self.https_proxy = https_proxy
        self.start()
        self.configure()
        self.tests = self.generate_test_list()

    def start(self):
        raise NotImplementedError( "Should have implemented a method to start the used engine" )

    def configure(self):
        raise NotImplementedError( "Should have implemented a method to configure the engine" )

    # def createsession(self):
    #     It is recommended to implement sessions to the test suite
    #

    def run_tests(self, targetURL):
        raise NotImplementedError( "Should have implemented a method to run all the tests from the engine" )

    def generate_test_list(self):
        raise NotImplementedError( "Should have implemented a method to return a list of Test objects" )

    def import_policy(self, path, name):
        raise NotImplementedError( "Should have implemented a method to return a list of Test objects" )


class Test(object):

    def __init__(self, name, testid, description, engine, vulnerability, tags, passed, enabled=True):
        self.name = name
        self.testid = testid
        self.description = description
        self.engine = engine
        self.vulnerability = vulnerability
        # Extra field for metadata
        self.tags = tags
        # If true the test successfully executed an exploit
        self.passed = passed
        self.enabled = enabled



