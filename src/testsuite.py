#!/usr/bin/env python


class TestSuite(object):
    """
    This class is abstract and serves as an interface to implement testing tools to the testing application.
    The testing application is composed by this interface interacting between a GUI and all the implemented tools.
    Required Functions:
    - start
    - configure
    - import_policy
    - generate_test_list
    - run_tests

    The above functions should run in the same order when used by the application

    For the time being it is also recommended to include a function to log in such that the tests can be performed
    within a session. However this is not part of the current implementation
    """

    def __init__(self, engine_name='Custom Engine', url=None, http_port=None, https_port=None):

        self.engine_name = engine_name
        self.url = url
        self.http_port = http_port
        self.https_port = https_port
        self.tests = []

    def start(self):
        """"
        Most testing tools needs to be started before they can be interacted with.
        Even if this is just a python module the class should be initiated here.
        """
        raise NotImplementedError( "Should have implemented a method to start the chosen engine" )

    def configure(self):
        """
        Run all configurations necessary to perform a test against the target.
        This function is mean to set up proxies or perform other configurations to the engine.
        """
        raise NotImplementedError( "Should have implemented a method to configure the engine" )

    # def createsession(self):
    #     It is recommended to implement sessions to the test suite
    #

    def generate_test_list(self):
        """
        This function must make a array of Test objects representing each of the tests that can be executed by the engine.
        The list must be compatible for the run_tests function
        :return:
        Array[Test...]
            List of Test objects
        """
        raise NotImplementedError( "Should have implemented a method to return a list of Test objects" )

    def import_policy(self, path, name):
        raise NotImplementedError( "Should have implemented a method to import the test policy from a file" )

    def run_tests(self, targetURL):
        raise NotImplementedError( "Should have implemented a method to run all the tests from the engine" )


class Test(object):

    def __init__(self, name, testid, description, engine, vulnerability, mode, passed, enabled=True):
        self.name = name
        self.testid = testid
        self.description = description
        self.engine = engine
        self.vulnerability = vulnerability
        # Extra field for metadata
        self.mode = mode
        # If true the test successfully executed an exploit
        self.passed = passed
        self.enabled = enabled



