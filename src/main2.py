#!/usr/bin/env python

from zaptestsuite import ZapTestSuite
import time

if __name__ == '__main__':
    testsuites = []
    testresults = []
    testsuites.append(ZapTestSuite("ZAP", 'http://127.0.0.1', '7576', '7576'))

    for test in testsuites:
        print("Running Test Suite", test.engine_name)
        test.start()
        # Delay further execution until engine is initiated
        # TODO: THIS IS NOT IDEAL
        time.sleep(30)
        print("ZAP BETTER BE DONE LOADING")
        print('------------------------------------------')
        print('------------------------------------------')
        print('------------------------------------------')
        print('------------------------------------------')
        print('------------------------------------------')
        print('------------------------------------------')
        print('------------------------------------------')
        print('------------------------------------------')
        print('------------------------------------------')
        print('------------------------------------------')
        print('------------------------------------------')
        print('------------------------------------------')
        print('------------------------------------------')
        print('------------------------------------------')
        print('------------------------------------------')
        print('------------------------------------------')
        print('------------------------------------------')
        print('------------------------------------------')
        print('------------------------------------------')
        test.configure()
        tests = test.generate_test_list()
        test.import_policy("path/to/policy", "Default Policy")
        testresults.extend(test.run_tests(tests, 'http://127.0.0.1:8080'))

    print("Test Results")
    for testres in testresults:
        print('------------------------------------------')
        #print(testres)
        
        print(testres.name, testres.testid, testres.engine, testres.vulnerability, testres.mode, testres.passed, testres.enabled)
