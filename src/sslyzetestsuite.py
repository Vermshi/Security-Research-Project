#!/usr/bin/env python

from testsuite import TestSuite, Test

class SSLyzeTestSuite(TestSuite):

    def start(self):
        raise NotImplementedError( "Should have implemented a method to start the used engine" )

    def configure(self):
        raise NotImplementedError( "Should have implemented a method to configure the engine" )

    def run_tests(self, targetURL):
        raise NotImplementedError( "Should have implemented a method to run all the tests from the engine" )

    def generate_test_list(self):
        raise NotImplementedError( "Should have implemented a method to return a list of Test objects" )

    def import_policy(self, path, name):
        raise NotImplementedError( "Should have implemented a method to import the test policy from a file" )


