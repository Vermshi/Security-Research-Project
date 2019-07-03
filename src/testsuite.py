#!/usr/bin/env python


class TestSuite(object):
    """
    This class is abstract and serves as an interface to implement testing tools to the testing application.
    The testing application is composed by this interface interacting between a GUI and all the implemented tools.
    Required Functions:
    - start
    - connect
    - import_policy
    - generate_test_list
    - run_tests

    The above functions should run in the same order when used by the application

    For the time being it is also recommended to include a function to log in such that the tests can be performed
    within a session. However this is not part of the current implementation

    :param engine_name: Name of the test engine
    :type engine_name: str
    """

    test_dictionary = {}

    def __init__(self, engine_name='Custom Engine'):
        self.engine_name = engine_name

    def start(self):
        """"
        Most testing tools needs to be started before they can be interacted with.
        Even if this is just a python module the class should be initiated here.
        """
        raise NotImplementedError( "Should have implemented a method to start the chosen engine" )

    def connect(self, scheme, address, port):
        """
        Run all configurations necessary to perform a test against the target. This function is mean to set up
        the connection to the target. The function should work for one or two specified ports if supported by engine

        :param address: Target IP or address
        :type address: str
        :param http_port: Target http port
        :type http_port: str
        :param https_port: Target https port
        :type https_port: str
        """
        raise NotImplementedError( "Should have implemented a method to configure the engine" )

    def generate_test_list(self):
        """
        This function must make a array of Test objects representing each of the tests that can be executed by the
        engine. The list must be compatible for the run_tests function

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

    def run_tests(self, tests):
        """
        Run all enabled tests against the target url with the http or https port specified in the connect function.
        The Test objects within the tests array describes each test. The array should be changed according to the
        outcome, and if both ports have been specified and are supported the results must be merged before returned.

        :param tests: Array of Test objects
        :type tests: Array[Test...]
        :param targetURL: The target including address and port
        :type targetURL: str
        :return: Array of test objects
        :rtype: Array[Test...]
        """
        raise NotImplementedError( "Should have implemented a method to run all the tests from the engine" )

    def stop(self):
        """
        Stop all running tests
        """
        raise NotImplementedError('May need to implemented method to stop running tests')

    def shutdown(self):
        """
        Some external engines needs to be properly shut down before closing the python program
        """
        raise NotImplementedError('May need to implemented method to shut down the engine properly')

    @staticmethod
    def get_tests_from_file(file, engine_name):
        # Retrieve extra information about the tests from the testfile
        test_file = open(file, "r")
        test_dictionary = {}
        for line in test_file:
            test_description = line.split(",")
            if engine_name == test_description[2]:
                # Maps the test name to vulnerability and difficulty
                test_dictionary[test_description[1]] = [test_description[0], int(test_description[3].strip("\n"))]
        return test_dictionary


class Test(object):
    """
    The Test object represent an individual test that can be executed by a test engine.

    :param name: The name of the test
    :type name: str
    :param testid: An id field which may be required by the engine to determine a test
    :type testid: int
    :param description: Description of the test, to be displayed as an explanation to the user
    :type description: str
    :param engine: The name of the engine running the test
    :type engine: str
    :param vulnerability: Describes which vulnerability the test reveals
    :type vulnerability: str
    :param mode: This field for metadata can be used by the engine to separate different categories
    :type mode: str
    :param difficulty: An int in the range 0-2 to describe the simplicity of a test
    :type difficulty: int
    :param passed: Determines whether the test was passed
    :type passed: bool
    :param enabled: Define if the test should be run or not
    :type enabled: bool
    """

    def __init__(self, name, testid, description, engine, vulnerability, mode, difficulty, passed, enabled=True):
        self.name = name
        self.testid = testid
        self.description = description
        self.engine = engine
        self.vulnerability = vulnerability
        self.mode = mode
        self.difficulty = difficulty
        self.passed = passed
        self.enabled = enabled
