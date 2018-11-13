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

    def __init__(self, engine_name='Custom Engine'):
        self.engine_name = engine_name

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

        :return: List of Test objects
        :rtype: Array[Test...]
        """
        raise NotImplementedError( "Should have implemented a method to return a list of Test objects" )

    def import_policy(self, path, name):
        """
        Import testing policy from file. This makes the initial configuration of which tests that are enabled.
        As well as other policies such as strength and sensitivity

        :param path: File path to config file
        :type path: str
        :param name: Policy name, may be useful for the engine
        :type name: str
        """
        raise NotImplementedError( "Should have implemented a method to import the test policy from a file" )

    def run_tests(self, tests, targetURL):
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
        raise NotImplementedError( "Should have implemented a method to run all the tests from the engine" )

    def shutdown(self):
        raise NotImplementedError( "Should have implemented a method to shut down the test enginge properly" )


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



