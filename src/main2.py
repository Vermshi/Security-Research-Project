#!/usr/bin/env python
from zaptestsuite import ZapTestSuite
import time

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
        test.connect('http://127.0.0.1', '8080')
        test.import_policy("testpolicy2.xml", 'testpolicy2')
        # Generate the test list after importing policy to reflect changes.
        tests = test.generate_test_list()
        testresults.extend(test.run_tests(tests))

    print("Test Results")
    for testres in testresults:
        print('------------------------------------------')

        print(testres.name, testres.testid, testres.engine, testres.vulnerability, testres.mode, testres.passed, testres.enabled)
