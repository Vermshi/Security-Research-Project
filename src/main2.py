#!/usr/bin/env python
from zaptestsuite import ZapTestSuite

"""
This code demonstrates use of all functions in the available test suites
"""

if __name__ == '__main__':
    testsuites = []
    testresults = []
    testsuites.append(ZapTestSuite("ZAP"))

    for test in testsuites:
        print("Running Test Suite", test.engine_name)
        test.start()
        test.configure()
        tests = test.generate_test_list()
        test.import_policy("path/to/policy", "Default Policy")
        testresults.extend(test.run_tests(tests, 'http://127.0.0.1:8080'))

    print("Test Results")
    for testres in testresults:
        print('------------------------------------------')

        print(testres.name, testres.testid, testres.engine, testres.vulnerability, testres.mode, testres.passed, testres.enabled)
