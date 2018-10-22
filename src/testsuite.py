#!/usr/bin/env python

import platform
import time

class TestSuite(object):
    """This class is abstract. The required functions are:"""

    def __init__(self, engine_name='Custom Engine', url=None, http_port=None, https_port=None):
        print("Initiate Test Suite")
        self.os = platform.system()
        self.engine_name = engine_name
        self.url = url
        self.http_port = http_port
        self.https_port = https_port
        self.tests = []

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
        raise NotImplementedError( "Should have implemented a method to import the test policy from a file" )


class Test(object):

    def __init__(self, name, testid, description, engine, vulnerability, mode, passed, enabled=True):
        self.name = name
        self.testid = testid
        self.description = description
        self.engine = engine
        self.vulnerability = vulnerability
        # Extra field for metadata
        self.mode = mode;
        # If true the test successfully executed an exploit
        self.passed = passed
        self.enabled = enabled



